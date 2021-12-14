/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2021 Lucas Czech

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact:
    Lucas Czech <lczech@carnegiescience.edu>
    Department of Plant Biology, Carnegie Institution For Science
    260 Panama Street, Stanford, CA 94305, USA
*/

#include "genesis/genesis.hpp"

#include <cmath>

using namespace genesis;
using namespace genesis::sequence;
using namespace genesis::utils;

std::string const header = R"###(<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
)###";

std::string const footer = R"###(
</body>
</html>
)###";

void html_color_char( char c, std::ostream& out )
{
    out << "<span class=\"";
    switch( c ) {
        case 'a':
        case 'A':
        case 'c':
        case 'C':
        case 'g':
        case 'G':
        case 't':
        case 'T': {
            out << "nt" << to_lower(c);
            break;
        }
        default: {
            out << "ntd";
        }
    }
    out << "\">" << c << "</span>";
}

void make_sequence_htmls( std::string const& base_path )
{
    auto const seq_file = base_path + "extern/dataForLucas/supergene.fasta";
    auto const out_dir = base_path + "data/sequences/";

    // line length
    size_t const ll = 100;

    auto const seqs = FastaReader().read( from_file( seq_file ));
    for( auto const& seq : seqs ) {
        std::ofstream out( out_dir + seq.label() + ".html" );

        out << header;
        out << "<span class=\"sequence\">";
        for( size_t i = 0; i < seq.length(); ++i ) {
            auto const c = seq[i];

            if( i % ll == 0 ) {
                if( i > 0 ) {
                    out << "<br />\n";
                }
                out << to_string_leading_zeros( i, std::ceil( std::log10( seq.length() ))) << " ";
            }
            html_color_char( c, out );
        }
        out << "</span>";
        out << footer;
    }
}

void pick_sites( std::string const& base_path )
{
    auto const seq_file = base_path + "extern/dataForLucas/supergene.fasta";
    auto const out_dir = base_path + "data/sequences/";

    // how many sites to pick
    size_t const ss = 10;

    // read alignment, and count uo the per site bases
    auto const seqs = FastaReader().read( from_file( seq_file ));
    auto const len = seqs[0].size();
    auto sc = SiteCounts( "ACGT", len );
    sc.add_sequences( seqs );

    // go through all sites, and compute their entropy
    auto entr = std::vector<double>( len );
    auto cnts = std::vector<size_t>( len );
    for( size_t i = 0; i < len; ++i ) {
        entr[i] = site_entropy( sc, i );

        // count how many determined sites there are in the alignment
        size_t cnt = 0;
        for( size_t j = 0; j < 4; ++j ) {
            cnt += sc.count_at( j, i );
        }
        cnts[i] = cnt;
        // std::cerr << cnt << "\n";
    }

    // find the sites with the highest entropy...
    auto const sort = sort_indices( entr.begin(), entr.end(), std::greater<double>() );
    auto snippets = std::vector<std::string>();

    // ...and print them in a list for each sequence
    std::ofstream out( out_dir + "list.html" );
    out << header;
    out << "<dl>\n";
    for( auto const& seq : seqs ) {
        out << "<dt>" << seq.label() << "</dt>";
        out << "<dd>";
        out << "<span class=\"sequence\">";

        // print the ss many first chars with the highest entropy
        // for( size_t i = 0; i < ss; ++i ) {
        //     auto const c = seq[ sort[i] ];
        //     html_color_char( c, out );
        // }

        // print the ss many first chars with the highest entropy
        // that have determined sites across all sequences
        size_t d = 0;
        size_t i = 0;
        std::string res;
        while( i < len && d < ss ) {
            // LOG_DBG << "i " << i << ", d " << d << ", cnts[i] " << cnts[i];
            if( cnts[sort[i]] != sc.added_sequences_count() ) {
                ++i;
                continue;
            }

            auto const c = seq[ sort[i] ];
            html_color_char( c, out );
            res += c;
            ++d;
            ++i;
        }
        snippets.push_back( res );

        out << "</span>";
        out << "</dd>\n";
    }
    out << "</dl>\n";
    out << footer;

    // check that all sequences are unique
    if( ! contains_duplicates( snippets ) ) {
        LOG_WARN << "not all unique!";
    }
}

int main( int argc, char** argv )
{
    (void) argc;
    (void) argv;

    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "started";

    std::string const base_path = "/home/lucas/Dropbox/GitHub/eseb-birds/";
    make_sequence_htmls( base_path );
    pick_sites( base_path );

    LOG_INFO << "finished";
    return 0;
}
