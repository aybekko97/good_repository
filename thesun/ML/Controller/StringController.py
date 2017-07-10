#!/usr/bin/env python
# -*- coding: utf-8 -*-
class StringController:
    @staticmethod
    #accepts number
    #return string of type str
    def int_to_hex(x):
        result = ""
        while x != 0:
            c = x % 16

            if c >= 10:
                result = chr(ord('A') + c - 10) + result
            else:
                result = chr(ord('0') + c) + result

            x /= 16
        return result

    #accepts string of type str
    #returns string of type str
    @staticmethod
    def to_utf8(s):
        i = 0
        result = ""
        while i < len(s):
            result += '%' + StringController.int_to_hex(ord(s[i]))
            i += 1
        return result

    #accepts json_object and key of type unicode
    #returns unicode
    @staticmethod
    def find_value_of_key(resp, key):
        if isinstance(resp, list):
            for item in resp:
                res = StringController.find_value_of_key(item, key)
                if res[0] == True:
                    return res

            return (False, "No value were found")

        if isinstance(resp, dict) == False:
            return (False, "No value were found")

        for k in resp:
            if k == key:
                return (True, resp[key])
            res = StringController.find_value_of_key(resp[k], key)
            if res[0] == True:
                return res

        return (False, "No value were found")

    #accepts two str
    #or two unicodes
    @staticmethod
    def lcs(given_str, to_find):
        n = len(given_str)
        m = len(to_find)

        d = [[0 for j in range(0, m + 1)] for i in range(0, n + 1)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                d[i][j] = max(d[i - 1][j], d[i][j - 1])
                if given_str[i - 1] == to_find[j - 1]:
                    d[i][j] = max(d[i][j], d[i - 1][j - 1] + 1)

        return d[n][m] == m

    @staticmethod
    def delete_symbols(given_str, symbols):
        result = ""
        for ch in given_str:
            if ch not in symbols:
                result += ch
        return result

    @staticmethod
    def before(given_str, to_find):
        result = ""
        for i in range(0, len(given_str)):
            found = True
            for j in range(0, len(to_find)):
                if i + j >= len(given_str):
                    found = False
                    break
                if given_str[i + j] != to_find[j]:
                    found = False
                    break
            if not found:
                result += given_str[i]
            else:
                break
        return result

    @staticmethod
    def after(given_str, to_find):
        for i in range(0, len(given_str)):
            found = True
            for j in range(0, len(to_find)):
                if i + j >= len(given_str):
                    found = False
                    break
                if given_str[i + j] != to_find[j]:
                    found = False
                    break
            if found:
                result = ""
                for j in range(i + len(to_find), len(given_str)):
                    result += given_str[j]
                return result
        return ""

    @staticmethod
    def delete_trailing_symbols(given_str, to_find):
        i = len(given_str) - 1
        while i >= 0:
            if given_str[i] not in to_find:
                result = ""
                for j in range(0, i + 1):
                    result += given_str[j]
                return result
            i -= 1
        return ""

    @staticmethod
    def delete_leading_symbols(given_str, to_find):
        for i in range(0, len(given_str)):
            if given_str[i] not in to_find:
                result = ""
                for j in range(i, len(given_str)):
                    result += given_str[j]
                return result
        return ""
