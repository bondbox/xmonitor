# coding:utf-8

from collections import namedtuple
from datetime import datetime
from enum import Enum
from io import TextIOWrapper
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from xml.etree.ElementTree import Element

from xarg import singleton
from xmanual import man

lr_file = namedtuple("logrotate_file", ("path", "desc"))


@singleton
class __lr_files():

    def __init__(self):
        self.__files: List[lr_file] = self.__get()
        self.__config: str = self.__get_default_config(self.__files)
        self.__status: str = self.__get_default_status(self.__files)

    def __iter__(self):
        return iter(self.__files)

    @property
    def config(self) -> str:
        return self.__config

    @property
    def status(self) -> str:
        return self.__status

    @classmethod
    def __get(cls) -> List[lr_file]:
        efiles: Optional[Element] = None
        for e in man.read_xml_tree("logrotate"):
            id = e.attrib.pop("id", None)
            if id == "files":
                assert e[0].tag == "title", f"{e[0].tag} != 'title'"
                assert e[0].text == "FILES", f"{e[0].text} != 'FILES'"
                efiles = e
                break
        assert isinstance(efiles, Element)

        etable: Optional[Element] = efiles.find("informaltable")
        assert isinstance(etable, Element)

        etgroup: Optional[Element] = etable.find("tgroup")
        assert isinstance(etgroup, Element)

        tbody: Optional[Element] = etgroup.find("tbody")
        assert isinstance(tbody, Element)

        rows: List[lr_file] = list()
        for row in tbody:
            efilename = row[0].find("filename")
            assert isinstance(efilename, Element)
            path = efilename.text
            desc = row[1].text
            assert isinstance(path, str), f"unexpected type {type(path)}"
            assert isinstance(desc, str), f"unexpected type {type(desc)}"
            rows.append(lr_file(path, desc))
        return rows

    @classmethod
    def __get_default_config(cls, files: List[lr_file]) -> str:
        path: Optional[str] = None
        for file in files:
            assert isinstance(file.path, str)
            if file.path.startswith("/etc") and "conf" in file.path:
                path = file.path
        assert isinstance(path, str)
        return path

    @classmethod
    def __get_default_status(cls, files: List[lr_file]) -> str:
        path: Optional[str] = None
        for file in files:
            assert isinstance(file.path, str)
            if file.path.startswith("/var") and "status" in file.path:
                path = file.path
        assert isinstance(path, str)
        return path


lr_files = __lr_files()


lr_status_v1 = namedtuple("logrotate_status_v1", ("path", "time"))
lr_status_v2 = namedtuple("logrotate_status_v2", ("path", "time"))
lr_state = lr_status_v1 | lr_status_v2


class lr_status():
    KEY_VAL = "items"
    KEY_VER_STR = "version"

    class versions(Enum):
        v1 = "logrotate state -- version 1"
        v2 = "logrotate state -- version 2"

    def __init__(self, path: str = lr_files.status):
        status = self.read(path)
        self.__version_str: str = status[lr_status.KEY_VER_STR]
        self.__items: List[lr_state] = status[lr_status.KEY_VAL]

    def __iter__(self):
        return iter(self.__items)

    @property
    def version(self) -> str:
        return self.__version_str

    @classmethod
    def read(cls, path: str) -> Dict[str, Any]:

        def __read_v1(hdl: TextIOWrapper) -> Dict[str, Any]:
            '''
            fprintf(f, "logrotate state -- version 1\n");

            for (i = 0; i < numStates; i++) {
            fprintf(f, "%s %d-%d-%d\n", states[i].fn, 
                states[i].lastRotated.tm_year + 1900,
                states[i].lastRotated.tm_mon + 1,
                states[i].lastRotated.tm_mday);
            }
            '''
            values: List[lr_status_v1] = list()
            status = {lr_status.KEY_VER_STR: "1", lr_status.KEY_VAL: values}
            for line in hdl.readlines():
                value = line.rstrip()
                items = value.rsplit(chr(32), 1)
                assert len(items) == 2
                path = items[0][1:-1]
                time = datetime.strptime(items[1], "%Y-%m-%d")
                values.append(lr_status_v1(path, time))
            return status

        def __read_v2(hdl: TextIOWrapper) -> Dict[str, Any]:
            '''
            bytes =  fprintf(f, "logrotate state -- version 2\n");
            if (bytes < 0)
                error = bytes;

            /*
            * Time in seconds it takes earth to go around sun.  The value is
            * astronomical measurement (solar year) rather than something derived from
            * a convention (calendar year).
            */
        #define SECONDS_IN_YEAR 31556926

            localtime_r(&nowSecs, &now);

            for (i = 0; i < hashSize && error == 0; i++) {
                for (p = states[i]->head.lh_first; p != NULL && error == 0;
                        p = p->list.le_next) {

                    /* Skip states which are not used for more than a year. */
                    now_time = mktime(&now);
                    last_time = mktime(&p->lastRotated);
                    if (!p->isUsed && difftime(now_time, last_time) > SECONDS_IN_YEAR) {
                        message(MESS_DEBUG, "Removing %s from state file, "
                                "because it does not exist and has not been rotated for one year\n",
                                p->fn);
                        continue;
                    }

                    error = fputc('"', f) == EOF;
                    for (chptr = p->fn; *chptr && error == 0; chptr++) {
                        switch (*chptr) {
                            case '"':
                            case '\\':
                                error = fputc('\\', f) == EOF;
                                break;
                            case '\n':
                                error = fputc('\\', f) == EOF;
                                if (error == 0) {
                                    error = fputc('n', f) == EOF;
                                }
                                continue;
                            default:
                                break;
                        }
                        if (error == 0 && fputc(*chptr, f) == EOF) {
                            error = 1;
                        }
                    }

                    if (error == 0 && fputc('"', f) == EOF)
                        error = 1;

                    if (error == 0) {
                        bytes = fprintf(f, " %d-%d-%d-%d:%d:%d\n",
                                        p->lastRotated.tm_year + 1900,
                                        p->lastRotated.tm_mon + 1,
                                        p->lastRotated.tm_mday,
                                        p->lastRotated.tm_hour,
                                        p->lastRotated.tm_min,
                                        p->lastRotated.tm_sec);
                        if (bytes < 0)
                            error = bytes;
                    }
                }
            }
            '''
            values: List[lr_status_v2] = list()
            status = {lr_status.KEY_VER_STR: "2", lr_status.KEY_VAL: values}
            for line in hdl.readlines():
                value = line.rstrip()
                items = value.split(chr(32))
                assert len(items) == 2
                assert items[0][0] == '"' and items[0][-1] == '"'
                path = items[0][1:-1]
                time = datetime.strptime(items[1], "%Y-%m-%d-%H:%M:%S")
                values.append(lr_status_v2(path, time))
            return status

        vers = {
            lr_status.versions.v1.value: __read_v1,
            lr_status.versions.v2.value: __read_v2,
        }

        with open(path) as hdl:
            ver = hdl.readline().strip()
            assert ver in vers, f"unkown version: '{ver}'"
            return vers[ver](hdl)
