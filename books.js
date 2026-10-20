/* ==========================================================================
   Lab 4b - Question 2: Retrieve and display JSON data
   Tan Yue Heng | AI240167
   ========================================================================== */

// Get the elements we will write the results into.
const firstTitle = document.getElementById("firstTitle");
const secondAuthor = document.getElementById("secondAuthor");
const genresList = document.getElementById("genres");
const errorBox = document.getElementById("error");

/*
   Load books.json with fetch().
   checkResponse.ok is false for 404s and other failed requests.
*/
fetch("books.json")
    .then(function (response) {
        if (!response.ok) {
            throw new Error("Could not load books.json (status " + response.status + ")");
        }
        // response.json() parses the text and fails if it is not valid JSON.
        return response.json();
    })
    .then(function (data) {
        // (a) Title of the first book
        firstTitle.textContent = data.books[0].title;

        // (b) Author of the second book
        secondAuthor.textContent = data.books[1].author;

        // (c) Genres of both books, grouped by book title
        data.books.forEach(function (book) {
            const li = document.createElement("li");
            li.textContent = book.title + " \u2014 " + book.genres.join(", ");
            genresList.appendChild(li);
        });
    })
    .catch(function (error) {
        // Show a friendly message instead of leaving the page blank.
        firstTitle.textContent = "";
        secondAuthor.textContent = "";
        errorBox.textContent =
            "Sorry, the book data could not be loaded. " + error.message;
    });
