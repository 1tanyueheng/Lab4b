/* ==========================================================================
   Lab 4b - Question 3: jQuery equivalents of three native JS operations
   Tan Yue Heng | AI240167
   ========================================================================== */

$(document).ready(function () {

    // (a) Native: document.getElementById("myElement").textContent = "Modified Text";
    $("#myElement").text("Modified Text");

    // (b) Native: document.querySelector("#myDIV").classList.add("myStyle");
    $("#myDIV").addClass("myStyle");

    // (c) Native: addEventListener("click", () => alert("Button clicked!"));
    $("#myButton").on("click", function () {
        alert("Button clicked!");
    });

});
