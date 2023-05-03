# TDP Hadoop Notes

The version 3.1.1-0.0 of Apache Hadoop is based on the `rel/release-3.1.1` tag of the Apache [repository](https://github.com/apache/hadoop/tree/rel/release-3.1.1).

## Jenkinfile

The file `./Jenkinsfile-sample` can be used in a Jenkins / Kubernetes environment to build and execute the unit tests of the Hadoop project. See []() for details on the environment.

## Making a release

```
mvn clean install -Pdist -Dtar -Pnative -DskipTests -Dmaven.javadoc.skip=true
```

`-Pdist -Dtar` generates a `.tar.gz` file of the release at `./hadoop-dist/target/hadoop-3.1.1-0.0.tar.gz`.

## Testing parameters

```
mvn -Ptest-patch -Pparallel-tests -Pshelltest -Pnative -Drequire.fuse -Drequire.openssl -Drequire.snappy -Drequire.valgrind -Drequire.zstd -Drequire.test.libhadoop -Dsurefire.rerunFailingTestsCount=3 -Pyarn-ui clean test --fail-never
```

- -Ptest-patch: will check that no new compiler warnings have been introduced by your patch
- -Pparallel-tests: By default, parallel-tests runs 4 test suites concurrently. This can be tuned by passing the testsThreadCount property.
-   -DtestsThreadCount=8
- -Pshelltest: Run shell tests
- -Pnative: Builds the Hadoop native libs (lz4, snappy, etc.)
- -Pyarn-ui: Builds the new YARN ui
- -Drequire.fuse:
- -Drequire.openssl: Fail if libcrypto.so is not found
- -Drequire.snappy: Fail if libsnappy.so is not found
- -Drequire.valgrind:
- -Drequire.zstd: Fail if libzstd.so is not found
- -Dsurefire.rerunFailingTestsCount: Retries failed test
- --fail-never: Does not interrupt the tests if one module fails

## Test execution notes

See `./test_notes.txt`
