
DROP TABLE IF EXISTS albums;

CREATE TABLE albums (
    id           INTEGER      PRIMARY KEY,
    id_artist    INTEGER,
    name         STRING (120),
    path_img     STRING (120),
    date_created TIMESTAMP    NOT NULL
                              DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO albums (
                       id,
                       id_artist,
                       name,
                       path_img,
                       date_created
                   )
                   VALUES (
                       1,
                       1,
                       'Joli Bebe',
                       '/static/covers/jolibb.jpg',
                       '2020-11-03 16:02:19'
                   );

INSERT INTO albums (
                       id,
                       id_artist,
                       name,
                       path_img,
                       date_created
                   )
                   VALUES (
                       2,
                       2,
                       'Ascend',
                       '/static/covers/ascend_coverArt.jpg',
                       '2020-11-03 16:45:46'
                   );

INSERT INTO albums (
                       id,
                       id_artist,
                       name,
                       path_img,
                       date_created
                   )
                   VALUES (
                       3,
                       2,
                       'Ashes',
                       '/static/covers/illenium_ashes.jpg',
                       '2020-11-15 01:19:32'
                   );



DROP TABLE IF EXISTS albums_liked;

CREATE TABLE albums_liked (
    id       INTEGER,
    id_user  INTEGER,
    id_album INTEGER,
    PRIMARY KEY (
        id
    )
);



DROP TABLE IF EXISTS artists;

CREATE TABLE artists (
    id       INTEGER      PRIMARY KEY,
    name     STRING (120),
    path_img STRING (120) 
);

INSERT INTO artists (
                        id,
                        name,
                        path_img
                    )
                    VALUES (
                        1,
                        'Naza',
                        '/static/imgArtists/naza.jpg'
                    );

INSERT INTO artists (
                        id,
                        name,
                        path_img
                    )
                    VALUES (
                        2,
                        'Illenium',
                        '/static/imgArtists/illenium.jpg'
                    );



DROP TABLE IF EXISTS artists_liked;

CREATE TABLE artists_liked (
    id        INTEGER PRIMARY KEY,
    id_user   INTEGER,
    id_artist INTEGER
);

INSERT INTO artists_liked (
                              id,
                              id_user,
                              id_artist
                          )
                          VALUES (
                              3,
                              6,
                              2
                          );


DROP TABLE IF EXISTS tracks;

CREATE TABLE tracks (
    id           INTEGER,
    id_album     INTEGER,
    id_artist    INTEGER,
    title        STRING (120),
    path_img     STRING (120),
    path_track   STRING (120),
    date_created TIMESTAMP     NOT NULL
                               DEFAULT CURRENT_TIMESTAMP,
    duration     VARCHAR (120),
    PRIMARY KEY (
        id
    )
);

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       1,
                       1,
                       1,
                       'Joli Bebe (ft. Niska)',
                       '/static/covers/jolibb.jpg',
                       '/static/track/Naza_(ft. Niska)_-_Joli_bebe.mp3',
                       '2020-11-02 13:01:20',
                       '02:53'
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       2,
                       2,
                       2,
                       'Sad Songs (ft. Said The Sky, Annika Wells)',
                       '/static/covers/ascend_coverArt.jpg',
                       '/static/track/ILLENIUM_Said The Sky_Annika_Wells_-_Sad_Songs.mp3',
                       '2020-11-03 15:54:38',
                       '03:31'
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       3,
                       2,
                       2,
                       'Gorgeous (ft. Bipolar Sunshine)',
                       '/static/covers/ascend_coverArt.jpg',
                       '/static/track/ILLENIUM_Blanke_Bipolar_Sunshine_-_Gorgeous.mp3',
                       '2020-11-10 21:35:26',
                       '04:38'
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       4,
                       2,
                       2,
                       'Angel (Lonely Prelude)',
                       '/static/covers/ascend_coverArt.jpg',
                       '/static/track/ILLENIUM_-_Angel_(Lonely_Prelude).mp3',
                       '2020-11-10 21:37:56',
                       '00:42'
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       5,
                       2,
                       2,
                       'Lonely (ft. Chandler Leighton)',
                       '/static/covers/ascend_coverArt.jpg',
                       '/static/track/ILLENIUM_Chandler_Leighton_-_Lonely.mp3',
                       '2020-11-10 21:38:39',
                       '04:32'
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       6,
                       3,
                       2,
                       'Reverie (feat. King Deco)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/01_Reverie_(feat_King_Deco).mp3',
                       '2020-11-14 14:38:22',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       7,
                       3,
                       2,
                       'Fortress (feat. Joni Fatora)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/02_Fortres_ (feat_Joni_Fatora).mp3',
                       '2020-11-14 14:38:23',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       8,
                       3,
                       2,
                       'With You (Quinn XCII)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/03_With_You_(Quinn_XCII).mp3',
                       '2020-11-14 14:38:23',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       9,
                       3,
                       2,
                       'Sleepwalker (feat. Joni Fatora)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/04_Sleepwalker_(feat_Joni_Fatora).mp3',
                       '2020-11-14 14:38:23',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       10,
                       3,
                       2,
                       'It''s All On U (feat. Liam O''Donnell)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/05_It''_s_All_On_U_(feat_Liam_O_Donnell).mp3',
                       '2020-11-14 14:38:23',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       11,
                       3,
                       2,
                       'Without You (feat. SKYLR)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/06_Without_You_(feat_SKYLR).mp3',
                       '2020-11-14 14:38:24',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       12,
                       3,
                       2,
                       'Spirals (feat. King Deco)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/07_Spirals_(feat_King_Deco).mp3',
                       '2020-11-14 14:38:24',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       13,
                       3,
                       2,
                       'Only One (feat. Nina Sung)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/08_Only_One_(feat_Nina_Sung).mp3',
                       '2020-11-14 14:38:25',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       14,
                       3,
                       2,
                       'I''ll Be Your Reason',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/09_I_ll_Be_Your_Reason.mp3',
                       '2020-11-14 20:57:06',
                       NULL
                   );

INSERT INTO tracks (
                       id,
                       id_album,
                       id_artist,
                       title,
                       path_img,
                       path_track,
                       date_created,
                       duration
                   )
                   VALUES (
                       15,
                       3,
                       2,
                       'Afterlife (feat. Echos)',
                       '/static/covers/illenium_ashes.jpg',
                       '/static/track/10_Afterlife_(feat_Echos).mp3',
                       '2020-11-14 20:57:06',
                       NULL
                   );


DROP TABLE IF EXISTS tracks_liked;

CREATE TABLE tracks_liked (
    id       INTEGER PRIMARY KEY,
    id_user  INTEGER,
    id_track INTEGER
);

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             1,
                             4,
                             1
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             2,
                             4,
                             2
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             3,
                             5,
                             1
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             5,
                             6,
                             4
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             7,
                             6,
                             13
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             8,
                             6,
                             8
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             10,
                             6,
                             9
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             11,
                             6,
                             3
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             12,
                             6,
                             6
                         );

INSERT INTO tracks_liked (
                             id,
                             id_user,
                             id_track
                         )
                         VALUES (
                             13,
                             6,
                             2
                         );



DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id              INTEGER,
    first_name      STRING (120),
    last_name       STRING (120),
    pseudo          STRING (120),
    email           STRING (120) UNIQUE,
    password        STRING (120),
    date_last_login TIMESTAMP    NOT NULL
                                 DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (
        id
    )
);

INSERT INTO users (
                      id,
                      first_name,
                      last_name,
                      pseudo,
                      email,
                      password,
                      date_last_login
                  )
                  VALUES (
                      6,
                      'eric',
                      'tran',
                      'huy',
                      'erictran@live.fr',
                      'sha1$BNFDqoT2$aa56aa89f9490789e605dd9ff36ac546df3c2dca',
                      '2020-11-16 09:09:12.191617'
                  );

