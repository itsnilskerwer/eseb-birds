// toggle_tree.js

function toggleTree() {
    var tree = document.getElementById("tree");
    // var text = document.getElementById("tree-text");
    var bottomButton = document.getElementById("bottom-toggle-button");
    if (tree.style.display === "none" || tree.style.display === "") {
        tree.style.display = "flex";
        // text.style.display = "flex";
        bottomButton.style.display = "flex";
    } else {
        tree.style.display = "none";
        // text.style.display = "none";
        bottomButton.style.display = "none";
    }
}
