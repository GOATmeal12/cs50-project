import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'practice.db')

# Connect to (or create) the database
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


cur.execute("""
INSERT INTO piano_works (composer, title) VALUES
-- Bach
('J.S. Bach', 'Minuet in G Major, BWV Anh. 114'),
('J.S. Bach', 'Minuet in G Minor, BWV Anh. 115'),
('J.S. Bach', 'Prelude in C Major, BWV 846'),
('J.S. Bach', 'Invention No. 1 in C Major, BWV 772'),
('J.S. Bach', 'Invention No. 4 in D Minor, BWV 775'),
('J.S. Bach', 'Invention No. 8 in F Major, BWV 779'),
('J.S. Bach', 'Sinfonia No. 1 in E-flat Major, BWV 787'),
('J.S. Bach', 'Prelude & Fugue in C Minor, WTC I'),
('J.S. Bach', 'Prelude & Fugue in D Major, WTC I'),
('J.S. Bach', 'Italian Concerto, BWV 971'),
('J.S. Bach', 'French Suite No. 5 in G Major, BWV 816'),
('J.S. Bach', 'Goldberg Variations'),
('J.S. Bach', 'Well-Tempered Clavier (Selections)'),

-- Beethoven
('L. van Beethoven', 'Für Elise'),
('L. van Beethoven', 'Sonatina in G Major, Anh. 5 No. 1'),
('L. van Beethoven', 'Sonatina in F Major, Anh. 5 No. 2'),
('L. van Beethoven', 'Piano Sonata No. 8 in C Minor "Pathétique"'),
('L. van Beethoven', 'Piano Sonata No. 14 in C-sharp Minor "Moonlight"'),
('L. van Beethoven', 'Piano Sonata No. 15 in D Major "Pastoral"'),
('L. van Beethoven', 'Piano Sonata No. 17 in D Minor "Tempest"'),
('L. van Beethoven', 'Piano Sonata No. 21 in C Major "Waldstein"'),
('L. van Beethoven', 'Piano Sonata No. 23 in F Minor "Appassionata"'),
('L. van Beethoven', 'Piano Sonata No. 29 in B-flat Major "Hammerklavier"'),
('L. van Beethoven', 'Rondo a Capriccio "Rage Over a Lost Penny"'),
('L. van Beethoven', 'Bagatelles (Selections)'),

-- Mozart
('W.A. Mozart', 'Minuet in F Major, K. 2'),
('W.A. Mozart', 'Minuet in G Major, K. 15'),
('W.A. Mozart', 'Sonata in C Major, K. 545'),
('W.A. Mozart', 'Rondo Alla Turca, K. 331'),
('W.A. Mozart', 'Fantasia in D Minor, K. 397'),
('W.A. Mozart', 'Variations on "Ah! vous dirai-je, Maman", K. 265'),

-- Clementi / Kuhlau / Diabelli
('M. Clementi', 'Sonatina in C Major, Op. 36 No. 1'),
('M. Clementi', 'Sonatina in G Major, Op. 36 No. 2'),
('M. Clementi', 'Sonatina in D Major, Op. 36 No. 3'),
('M. Clementi', 'Sonatina in F Major, Op. 36 No. 4'),
('F. Kuhlau', 'Sonatina in C Major, Op. 20 No. 1'),
('A. Diabelli', 'Sonatina in C Major, Op. 168 No. 1'),

-- Burgmüller / Czerny / Hanon
('F. Burgmüller', 'Arabesque, Op. 100 No. 2'),
('F. Burgmüller', 'Ballade, Op. 100 No. 15'),
('F. Burgmüller', '25 Easy and Progressive Studies, Op. 100'),
('C. Czerny', 'The School of Velocity, Op. 299'),
('C. Czerny', 'The School of Mechanism, Op. 821'),
('C. Czerny', 'Art of Finger Dexterity, Op. 740'),
('C.L. Hanon', 'The Virtuoso Pianist'),

-- Chopin — INDIVIDUAL WALTZES
('F. Chopin', 'Waltz in E-flat Major, Op. 18 "Grande Valse Brillante"'),
('F. Chopin', 'Waltz in A-flat Major, Op. 34 No. 1'),
('F. Chopin', 'Waltz in A Minor, Op. 34 No. 2'),
('F. Chopin', 'Waltz in F Major, Op. 34 No. 3'),
('F. Chopin', 'Waltz in A-flat Major, Op. 42'),
('F. Chopin', 'Waltz in D-flat Major, Op. 64 No. 1 "Minute"'),
('F. Chopin', 'Waltz in C-sharp Minor, Op. 64 No. 2'),
('F. Chopin', 'Waltz in A-flat Major, Op. 64 No. 3'),
('F. Chopin', 'Waltz in A Minor, Op. posth.'),

-- Chopin — Other Core Works
('F. Chopin', 'Prelude in E Minor, Op. 28 No. 4'),
('F. Chopin', 'Nocturne in E-flat Major, Op. 9 No. 2'),
('F. Chopin', 'Fantaisie-Impromptu, Op. 66'),
('F. Chopin', 'Ballade No. 1 in G Minor, Op. 23'),
('F. Chopin', 'Scherzo No. 2 in B-flat Minor, Op. 31'),
('F. Chopin', 'Polonaise in A-flat Major, Op. 53'),
('F. Chopin', 'Études, Op. 10 (Selections)'),
('F. Chopin', 'Études, Op. 25 (Selections)'),

-- Schumann / Schubert / Mendelssohn
('R. Schumann', 'Kinderszenen, Op. 15'),
('R. Schumann', 'Scenes from Childhood'),
('R. Schumann', 'Fantasie in C Major, Op. 17'),
('F. Schubert', 'Impromptu in G-flat Major, Op. 90 No. 3'),
('F. Schubert', 'Impromptus, Op. 90'),
('F. Schubert', 'Wanderer Fantasy'),
('F. Mendelssohn', 'Songs Without Words (Selections)'),

-- Debussy / Ravel
('C. Debussy', 'Clair de Lune'),
('C. Debussy', 'Arabesque No. 1'),
('C. Debussy', 'Rêverie'),
('C. Debussy', 'The Little Negro'),
('M. Ravel', 'Pavane pour une infante défunte'),
('M. Ravel', 'Jeux d’eau'),
('M. Ravel', 'Gaspard de la nuit'),

-- Romantic / Late Romantic
('F. Liszt', 'Liebesträume No. 3'),
('F. Liszt', 'Consolation No. 3'),
('F. Liszt', 'Hungarian Rhapsody No. 2'),
('F. Liszt', 'Piano Sonata in B Minor'),
('J. Brahms', 'Intermezzi, Op. 117'),
('J. Brahms', 'Waltz in A-flat Major, Op. 39 No. 15'),
('S. Rachmaninoff', 'Prelude in C-sharp Minor, Op. 3 No. 2'),
('S. Rachmaninoff', 'Prelude in G Minor, Op. 23 No. 5'),

-- Modern / Contemporary
('E. Satie', 'Gymnopédie No. 1'),
('E. Satie', 'Gnossienne No. 1'),
('P. Glass', 'Metamorphosis'),
('L. Einaudi', 'Nuvole Bianche'),
('L. Einaudi', 'Una Mattina'),
('Yiruma', 'River Flows in You'),
('Yiruma', 'Kiss the Rain'),
('Yann Tiersen', 'Comptine d’un autre été'),

-- Misc / Anthology / Arrangements
('Traditional', 'Christmas Favorites (arr.)'),
('Traditional', 'Hymns (arr.)'),
('Various', 'Jazz Standards (solo piano arrangements)'),
('Various', 'Movie Themes (solo piano arrangements)');

""")



conn.commit()
conn.close()