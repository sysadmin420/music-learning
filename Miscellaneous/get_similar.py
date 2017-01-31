######################
## take a list of spotify tracks and
## given one track from the list,
## output the most similar tracks to it
## according to audio feature metadata
######################

import sys
import pdb
sys.path.append( "../Modules")
import spotify_methods as sp
import data_methods as dam
import helpers as hlpr


def main():

    genres = True

    ## get subset of db based on input.txt
    db, unfound_tracks = hlpr.processInput(genres = genres)

    cols_to_remove = ["spotify_id", "spotify_album_id", "echonest_id", "title",
                      "album", "artist", "echonest_artist_id",
                      "spotify_artist_id", "duration", "time_signature",
                      "loudness", "release_date", "year"]
    ## "_freqwt" is overkill for the sake of explicitness
    ## as "_freq" is in "_freqwt"
    substr_cols_to_remove = ["_freqwt", "_freq"]
    X = hlpr.dataFrameToMatrix(db, cols_to_remove, substr_cols_to_remove,
                               fillNA = True, centerScale = True)

    ## create directed walk starting at song from sys args
    artist = raw_input('Enter artist name: ')
    song = raw_input('Enter song name: ')

    neighbors = dam.getSimilarPoints(X.copy(), db, artist, song, 10)
    print neighbors


if __name__ == "__main__":
    main()
