console.log('this is ecomerce page ');
let basePrice = document.getElementById('basePrice').innerText;

basePrice = Number(basePrice);

let quantity = document.getElementById('quantity').innerText;

quantity = Number(quantity);

let price = document.getElementById('price').innerText;
price = Number(price); //use to convert string into Number
document.getElementById('price').innerText = basePrice * quantity;

 let gst = document.getElementById('gst').innerText;
 gst = Number(gst);

 let GrandTotal =  document.getElementById('GrandTotal').innerText;
 GrandTotal = Number(GrandTotal);

