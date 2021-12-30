# The `keylix` pattern specification

Last updated: *2021-12-30*

This page describes the `keylix-v0.1.x` pattern specification.

### Introduction

`keylix` is a simple GLOB-like string matching pattern specification intended for searching elements in lists of short strings (keys).

*Note: The name `keylix` is an abbreviation for "key list expressions."*

For example, pattern `cherries` matches any string that contains the word "cherries," and `apples | oranges` matches any string that contains "apples" or "oranges."
Similarly, `raspberries & pies` matches any string that both "raspberries" and "pies."
Pattern `pineapples & ~(peanuts)` matches strings that contain "pineapples" but do not contain the word "peanuts."