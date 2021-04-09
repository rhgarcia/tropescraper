#!/usr/bin/env raku

use JSON::Fast;



my $json-file-name = @*ARGS[0] // "tvtropes.json";

my %links = from-json $json-file-name.IO.slurp;

say "Movie;Tropes";
for %links.kv -> $key, @values {
    say "$key; ", @values.join(",");
}
