#!/usr/bin/env raku

use JSON::Fast;



my $json-file-name = @*ARGS[0] // "tvtropes.json";

my %links = from-json $json-file-name.IO.slurp;

for %links.keys.sort: { %links{$^b}.elems <=> %links{$^a}.elems } -> $k {
    say "$k, { %links{$k}.elems }";
}


    
