pypular
=======

The purpose of this tool is to download python packages from PYPI multiple times, to inflate the download counter.


How to use?
-----------

`pypular https://bla.com/bla.whl 300`


But why?
--------

This started with my [talk](https://codeberg.org/ltworf/pages/src/branch/master/owasp2024) about the security measures of PYPI.

Since for a while PYPI required stricter security for packages with an higher download count, I wanted to prove that download count is a bad measure.

Briefly after my talk, Snyk removed the download plot of python packages, but keeps using the count as a metric to evaluate quality. I don't know if this was related.

It is well known that the download counter is highly inaccurate (can be inflated artificially, doesn't take into account cached downloads, distributions, mirrors) and yet is taken into heavy consideration. I see no problem to play with it since it's a bad metric to begin with.

Packages used by more skilled people end up having a lower download count and their popularity will be under reported. On the other hand, people who won't bother with setting up a cache or reusing a container image, or use a distribution will inflate the counters of some other packages, downloading them multiple times with their CI.

It is my opinion that google and microsoft discourage caching the downloads to obtain metrics. It costs both of them bandwidth to do so, but I presume the information is more valuable than the cost.

I doubt I'm the first one to think about inflating the download counter to gain fake popularity. But to the best of my knowledge I'm the first one to publish a tool to do it easily.

Donate
======
[Donate](https://liberapay.com/ltworf/donate)
