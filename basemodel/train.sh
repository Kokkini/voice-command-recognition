#!/bin/bash

# before running, do the following:
# Make a copy of basemodel
# copy the newly generated .fileids and .transcription there
# copy the training data there

sphinx_fe -argfile en-us/feat.params \
        -samprate 16000 -c anno.fileids \
       -di . -do . -ei wav -eo mfc -mswav yes

./bw/bw \
 -hmmdir en-us \
 -moddeffn en-us/mdef.txt \
 -ts2cbfn .ptm. \
 -feat 1s_c_d_dd \
 -svspec 0-12/13-25/26-38 \
 -cmn current \
 -agc none \
 -dictfn cmudict-en-us.dict \
 -ctlfn anno.fileids \
 -lsnfn anno.transcription \
 -accumdir .

./mllr_solve/mllr_solve \
    -meanfn en-us/means \
    -varfn en-us/variances \
    -outmllrfn mllr_matrix -accumdir .

cp -a en-us en-us-adapt

./map_adapt/map_adapt \
    -moddeffn en-us/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn en-us/means \
    -varfn en-us/variances \
    -mixwfn en-us/mixture_weights \
    -tmatfn en-us/transition_matrices \
    -accumdir . \
    -mapmeanfn en-us-adapt/means \
    -mapvarfn en-us-adapt/variances \
    -mapmixwfn en-us-adapt/mixture_weights \
    -maptmatfn en-us-adapt/transition_matrices