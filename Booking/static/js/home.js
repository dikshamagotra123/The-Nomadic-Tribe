// window.onload = (event) => {
//     var default_price = document.getElementById('default_price').innerHTML;
//     document.getElementById("form").onchange = function (e) {
//         var form = e.target.form;
//         console.log(form["checkin"].value, form["checkout"].value);
//         checkin_date = new Date(form["checkin"].value);
//         checkout_date = new Date(form["checkout"].value);
//         no_of_nights = Math.abs(checkout_date - checkin_date) / 86400000;
//         price = text;

//         no_of_rooms = parseInt(form["quantity"].value);
//         function get_price(no_of_nights, no_of_rooms, price) {
//             final_price = no_of_rooms * no_of_nights * price;
//             return final_price;
//         }
//         $("#price").val(get_price(no_of_nights, no_of_rooms, price));
//     };

//     var today = new Date();
//     var dd = String(today.getDate()).padStart(2, "0");
//     var mm = String(today.getMonth() + 1).padStart(2, "0");
//     var yyyy = today.getFullYear();

//     today = yyyy + "-" + mm + "-" + dd;
//     $("#checkin").attr("min", today);
//     $("#checkout").attr("min", today);
// };