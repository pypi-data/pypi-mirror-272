#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def pkg_fun01():
    info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " => this is package demo function"
    print(info)
    return info


def main():
    print(pkg_fun01())


if __name__ == "__main__":
    main()