Check environment variables:

  $ echo "$LANG"
  C
  $ echo "$LC_ALL"
  C
  $ echo "$LANGUAGE"
  C
  $ echo "$TZ"
  GMT
  $ echo "$CDPATH"
  
  $ echo "$GREP_OPTIONS"
  
  $ echo "$PRYSK_TEMP"
  .+ (re)
  $ echo "$TESTDIR"
  */examples (glob)
  $ ls "$TESTDIR"
  bare.t
  empty.t
  env.t
  fail.t
  missingeol.t
  skip.t
  test.t
  $ echo "$TESTFILE"
  env.t
  $ echo "$TMPDIR/x/y"
  $TMPDIR/x/y
  $ echo "$TMP/foo/bar"
  $TMPDIR/foo/bar
  $ pwd
  */prysk-tests*/env.t (glob)
