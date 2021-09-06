<script>
  let cart = [];

  $: price = cart.reduce(
    (acc, cartItem) => acc + cartItem.price * cartItem.quantity,
    0
  );
  $: setPrice(price);
  let amount = 1;
  $: priceWithQuantity = price * amount;
  $: console.log(priceWithQuantity);
  $: console.log({ cart });
  window.renderCartItems = renderCartItems;
  // $: document.querySelector(".cart-summary").textContent = price;

  function renderCartItems() {
    console.log(cart.length);
    // if (cart.length === 0) {
    //   document.querySelector(
    //     ".cart-full.pb-sm-4.mb-4"
    //   ).innerHTML = `<h1>Пусто</h1>`;
    //   return;
    // }

    const cartHtml = cart
      .map((cartItem) => {
        return `<div class="cart-item">
              <div class="cart-item_imgwrapper">
                  <img class="cart-item_img" src='${cartItem.img}'/>
              </div>
              <div class="cart-item_title">${cartItem.name}</div>
              <div class="calculation-wrap">
                  <div class="calculations">
                      <div class="minus-btn">-</div>
                      <div class="item-quantity">${cartItem.quantity}</div>
                      <div class="plus-btn">+</div>
                  </div>
              </div>
              <div class="cart-item_price text-right">${cartItem.price}.-</div>
          </div>`;
      })
      .join("");
    document
      .querySelectorAll(".cart-full")
      .forEach((el) => (el.innerHTML = cartHtml));

    document
      .querySelectorAll(
        ".cart-item > .calculation-wrap>.calculations >.plus-btn"
      )
      .forEach(
        (el) =>
          (el.onclick = (e) => {
            const cartItem = e.target.parentNode.parentNode.parentNode;
            const quantityEl = cartItem.querySelector(".item-quantity");
            quantityEl.textContent = Number(quantityEl.textContent) + 1;
            const cartName = cartItem.querySelector(
              ".cart-item > .cart-item_title"
            ).textContent;
            cart = cart.map((ci) => {
              if (ci.name === cartName) {
                ci.quantity += 1;
                const quantityEl = document
                  .getElementById(ci.id)
                  .querySelector(".item-quantity");
                quantityEl.textContent = Number(quantityEl.textContent) + 1;
              }

              return ci;
            });
          })
      );

    document
      .querySelectorAll(
        ".cart-item > .calculation-wrap>.calculations >.minus-btn"
      )
      .forEach(
        (el) =>
          (el.onclick = (e) => {
            const cartItem = e.target.parentNode.parentNode.parentNode;
            const quantityElInCart = cartItem.querySelector(".item-quantity");
            // quantityEl.textContent = Number(quantityEl.textContent) - 1;
            const cartName = cartItem.querySelector(
              ".cart-item > .cart-item_title"
            ).textContent;
            cart = cart.map((ci) => {
              if (ci.name === cartName && ci.quantity !== 0) {
                ci.quantity -= 1;
                const quantityEl = document
                  .getElementById(ci.id)
                  .querySelector(".item-quantity");
                quantityEl.textContent = ci.quantity;
                quantityElInCart.textContent = ci.quantity;
              }

              return ci;
            });
          })
      );
    // setPrice();
  }

  function getPrice(parentNode) {
    try {
      return Number(
        parentNode.parentNode
          .querySelector(".dish-details_price")
          ?.textContent.slice(0, -2)
          .replace(",", ".")
      );
    } catch (err) {}
  }

  function setPrice() {
    try {
      document.querySelector(".cart-summary").textContent = price + ".-";
    } catch (err) {
      // console.log("start", priceWithQuantity);
      setTimeout(() => {
        document.querySelector(".delivery-title b").textContent =
          priceWithQuantity + ".-";
        document.querySelector(".cart-summary_amount.text-right").textContent =
          priceWithQuantity + ".-";
      }, 0);
    }
  }

  document
    .querySelectorAll(".minus-btn")
    .forEach((elem) =>
      elem.addEventListener("click", (e) => handleClickOnMinus(e))
    );
  document
    .querySelectorAll(".plus-btn")
    .forEach((elem) =>
      elem.addEventListener("click", (e) => handleClickOnPlus(e))
    );
  function handleClickOnMinus(e) {
    const parentNode = e.target.parentNode;
    const quantity = parentNode.querySelector(".item-quantity").innerText;
    const productCard = e.target.parentNode.parentNode.parentNode;

    if (productCard.id === "order-data") {
      if (parseInt(quantity) === 1 || amount === 1) return;

      const quantityEl = parentNode.querySelector(".item-quantity");
      amount -= 1;
      quantityEl.innerText = amount;
      // setPrice();
      return;
    }

    if (parseInt(quantity) === 0) return;

    const productIndex = cart.findIndex((el) => {
      return el.name === productCard.querySelector(".dish-title").textContent;
    });

    cart = cart.map((el, i) => {
      if (i === productIndex) el.quantity -= 1;
      return el;
    });

    parentNode.querySelector(".item-quantity").innerText =
      parseInt(quantity) - 1;
    const menuItemPrice = getPrice(parentNode);
    if (menuItemPrice) price -= menuItemPrice;
    // setPrice();
    renderCartItems();
    // document.querySelector('.cart-full.pb-sm-4.mb-4').innerHTML=
  }

  function handleClickOnPlus(e) {
    const parentNode = e.target.parentNode;
    const productCard = e.target.parentNode.parentNode.parentNode;

    const menuItemPrice = getPrice(parentNode);
    if (productCard.id === "order-data") {
      const quantityEl = parentNode.querySelector(".item-quantity");
      amount += 1;
      quantityEl.innerText = amount;
      // setPrice();
      return;
    }

    const productIndex = cart.findIndex((el) => {
      return el.name === productCard.querySelector(".dish-title").textContent;
    });

    if (productIndex !== -1) {
      cart = cart.map((el, i) => {
        if (i === productIndex) el.quantity += 1;
        return el;
      });
    } else {
      cart = [
        ...cart,
        {
          price: menuItemPrice,
          name: productCard.querySelector(".dish-title").textContent,
          quantity: 1,
          img: productCard.querySelector(".dish-img").getAttribute("src"),
          id: productCard.id,
        },
      ];
    }

    price += menuItemPrice;

    // let quantity = parentNode.querySelector(".item-quantity").innerText;
    // setPrice();
    parentNode.querySelector(".item-quantity").innerText =
      cart[productIndex]?.quantity || cart[cart.length - 1].quantity;
    renderCartItems();
  }
</script>
