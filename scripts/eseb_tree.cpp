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

using namespace genesis;
using namespace genesis::placement;
using namespace genesis::tree;
using namespace genesis::utils;

Tree create_random_tree( std::vector<std::string> const& names )
{
    auto tree = minimal_tree();

    // The minimal tree already has 2 leaves. Create the remaining ones.
    for( size_t i = 2; i < names.size(); ++i ) {
        // Pick a random edge to attach the leaf to.
        auto& rand_edge = tree.edge_at( std::rand() % tree.edge_count() );
        add_new_leaf_node( tree, rand_edge );
    }
    LOG_INFO << "Names: " << names.size();
    // LOG_INFO << "Leaves: " << leaf_node_count( tree );

    // Give names to the leaf nodes.
    size_t leaf_node_cnt = 0;
    for( auto& node : tree.nodes() ) {
        if( is_leaf( node )) {
            node.data<CommonNodeData>().name = names[leaf_node_cnt];
            ++leaf_node_cnt;
        }
    }

    // Give random edge lengths in [ 0.0, 1.0 ] to all edges.
    for( auto& edge : tree.edges() ) {
        auto const bl = static_cast<double>( std::rand() ) / static_cast<double>( RAND_MAX );
        edge.data<CommonEdgeData>().branch_length = bl;
    }

    // Reroot on random inner node.
    size_t rand_node_index = 0;
    while( is_leaf( tree.node_at( rand_node_index ))) {
        rand_node_index = std::rand() % tree.node_count();
    }
    change_rooting( tree, tree.node_at( rand_node_index ));

    return tree;
}

void make_svg_image_tree( Tree const& tree, std::string const& out_path )
{
    // Base path for the svg links. Set to relative to work with shifting dirs.
    // std::string const base_path = out_path;
    std::string const base_path = "../";

    // Make a layout tree. We make a copy without taxon names,
    // to avoid having those show up in the svg.
    auto copy = tree;
    for( auto& node : copy.nodes() ) {
        node.data<CommonNodeData>().name = "";
    }

    auto layout = tree::RectangularLayout( copy, tree::LayoutType::kPhylogram );
    layout.height( 40.0 * tree.node_count() );

    // Add node shapes
    std::vector<utils::SvgGroup> node_shapes;
    node_shapes.resize( tree.node_count() );
    for( size_t i = 0; i < tree.node_count(); ++i ) {
        if( ! is_leaf( tree.node_at(i) )) {
            continue;
        }

        // Use the taxon name to get the image, and add it.
        auto const& taxon = tree.node_at(i).data<CommonNodeData>().name;
        auto const image_file = base_path + "data/thumbs/" + taxon + ".png";
        // if( ! file_exists( image_file )) {
        //     LOG_WARN << "File not found: " << image_file;
        // }
        node_shapes[i].add( utils::SvgImage(
            image_file,
            10, -50, 100, 100
        ));

        // Also add a hyperlink to the taxon sub page.
        auto const html_file = base_path + "species/" + taxon + ".html";
        // if( ! file_exists( html_file )) {
        //     LOG_WARN << "File not found: " << html_file;
        // }
        node_shapes[i].set_hyperlink({
            { "href", html_file },
            { "target", "_blank" }
        });
    }
    layout.set_node_shapes( node_shapes );

    // Set edge strokes.
    std::vector<utils::SvgStroke> strokes;
    for( size_t i = 0; i < tree.edge_count(); ++i ) {
        (void) i;
        auto stroke = SvgStroke();
        stroke.line_cap = utils::SvgStroke::LineCap::kRound;
        stroke.width = 6.0;
        strokes.push_back( std::move( stroke ));
    }
    layout.set_edge_strokes( strokes );

    // Write to file
    std::ostringstream out;
    layout.to_svg_document().write( out );
    utils::file_write( out.str(), out_path + "tree/tree.svg" );
}

int main( int argc, char** argv )
{
    (void) argc;
    (void) argv;

    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "started";

    // Input data. Hard coded for now.
    // if( argc != 2 ) {
    //     throw std::runtime_error( "need input files" );
    // }
    std::string const base_path = "/home/lucas/Dropbox/GitHub/eseb-birds/";
    std::string const taxon_names_file = base_path + "data/names.txt";
    std::string const newick_file = base_path + "tree/tree.newick";

    // Load the tree, or make it randomly.
    Tree tree;
    if( is_file( newick_file )) {
        tree = CommonTreeNewickReader().read( from_file( newick_file ));
    } else {
        // Get a list of taxon names, and make a random tree from them.
        auto const taxon_names = file_read_lines(taxon_names_file);
        tree = create_random_tree( taxon_names );

        // Write the tree, for next usage.
        CommonTreeNewickWriter().write( tree, to_file( newick_file ));
    }

    // Make an svg tree out of it and save it.
    make_svg_image_tree( tree, base_path );

    LOG_INFO << "finished";
    return 0;
}
