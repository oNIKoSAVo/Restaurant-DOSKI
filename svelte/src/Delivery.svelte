<script>
  let cart = [];

  $: price = cart.reduce(
    (acc, cartItem) => acc + cartItem.price * cartItem.quantity,
    0
  );
  $: grams = cart.reduce(
    (acc, cartItem) => acc + cartItem.grams * cartItem.quantity,
    0
  );
  $: setPrice(price, grams, peopleQuantity);
  let peopleQuantity = 1;
  $: console.log({ cart });
  window.renderCartItems = renderCartItems;

  // $: document.querySelector(".cart-summary").textContent = price;

  function renderCartItems() {
    cleanCart();

    console.log("length", cart.length);

    [...document.querySelectorAll("#cart .stage")].map((s, i) => {
      if (i === 0) {
        s.style = "display: block;";
      } else {
        s.style = "display: none;";
      }
      return s;
    });
    let cartHtml;
    console.log(cart.length > 0);
    if (cart.length > 0) {
      document.querySelector(".cart-sum").classList.remove("d-none");
      cartHtml = cart
        .map((cartItem) => {
          return `<div class="cart-item" data-id="${cart.id}">
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
              <div class="cart-item_price text-right">${cartItem.price}₽</div>
          </div>`;
        })
        .join("");
      console.log("price>0", price > 0);
      const cartSumContainer = document.querySelector(".cart-sum");
      const cartSum = document.querySelector(".cart-summary_amount.text-right");
      // if (cart. > 0) {
      //   console.log(cartSumContainer);
      //   cartSumContainer.classList.remove("d-none");
      // } else {
      //   cartSumContainer.classList.add("d-none");
      // }
    } else {
      cartHtml = "<h1>Корзина пуста</h1>";
      document.querySelector(".cart-sum").classList.add("d-none");
    }

    document
      .querySelectorAll(".cart-full")
      .forEach((el) => (el.innerHTML = cartHtml));
    console.log(document.querySelectorAll(".cart-full"));

    [
      ...document.querySelectorAll(
        ".cart-item > .calculation-wrap>.calculations >.plus-btn"
      ),
    ].forEach(
      (el) =>
        (el.onclick = (e) => {
          const cartItem = e.target.closest(".cart-item");
          const cartName = cartItem.querySelector(
            ".cart-item > .cart-item_title"
          ).textContent;
          const cartQuantityEl = cartItem.querySelector(".item-quantity");
          cart = cart.map((ci) => {
            if (ci.name === cartName) {
              ci.quantity += 1;
              const quantityEl = document
                .getElementById(ci.id)
                .querySelector(".item-quantity");
              quantityEl.textContent = cartQuantityEl.textContent = ci.quantity;
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
            const lastCart = [...cart];
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
            cleanCart();
            if (lastCart.length !== cart.length) renderCartItems();
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
//TODO refactoring
  function setPrice() {
    const deliveryTitlePrice = document.querySelector(".delivery-title b");
      const cartSummaryPrice = document.querySelector(
          "#preorder .cart-summary_amount.text-right"
      );
    try {
      document.querySelector(".cart-summary").textContent =
        document.querySelector(".cart-summary_amount").textContent =
          price + "₽";

      if (!deliveryTitlePrice || !cartSummaryPrice) return;
      deliveryTitlePrice.textContent = cartSummaryPrice.textContent =
        price + "₽";
      console.log({
        cs: document.querySelector(".cart-summary_amount.text-right"),
      });
      document.querySelector(".gram b").textContent = `${Math.round(
        grams / peopleQuantity
      )}гр`;
    } catch (err) {
        console.log('catch')
        // console.log("start", price);
      setTimeout(() => {
        if (deliveryTitlePrice) {
          deliveryTitlePrice.textContent = price + "₽";
        }
        if (document.querySelector(".cart-summary_amount.text-right") && cartSummaryPrice) {
          document.querySelector(
            ".cart-summary_amount.text-right"
          ).textContent = cartSummaryPrice.textContent=price + "₽";
        }
        if (document.querySelector(".gram b")) {
          document.querySelector(".gram b").textContent = `${Math.round(
            grams / peopleQuantity
          )}гр`;
        }

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

  document.addEventListener("DOMContentLoaded", () => {
    document
      .querySelector(".checkout-final")
      .addEventListener("click", async () => {
        const fio = document
          .querySelector("#checkoutform input[name='name']")
          .value.trim();
        const address = document
          .querySelector("#checkoutform input[name='addres']")
          .value.trim();
        const phone = document
          .querySelector("#checkoutform input[name='phone']")
          .value.trim();
        const comment = document
          .querySelector("#checkoutform input[name='comment']")
          .value.trim();
        const paymentType = document
          .querySelector("#checkoutform select[name='paymentType']")
          .value.trim();
        if (!fio || !address || !phone) return;
        const payload = {
          fio,
          address,
          phone,
          comment,
          paymentType,
          menue: cart,
        };

        const response = await fetch("/create_order", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (result.payment_url) {
          window.location.href = result.payment_url;
        }
      });
    //modal btns
    document.querySelector("#item-buy .plus-btn").onclick = (e) => {
      const modal = document.querySelector("#item-buy");
      const modalName = modal.querySelector(".modal-title").textContent;
      const modalQuantityEl = modal.querySelector(".item-quantity");

      const productIndex = cart.findIndex((el) => {
        return el.name === modalName;
      });

      if (productIndex !== -1) {
        cart = cart.map((ci) => {
          if (ci.name === modalName) {
            console.log(ci);
            ci.quantity += 1;
            const quantityEl = document
              .getElementById(ci.id)
              .querySelector(".item-quantity");
            quantityEl.textContent = modalQuantityEl.textContent = ci.quantity;
          }
          return ci;
        });
      } else {
        cart = [
          ...cart,
          {
            price: Number(
              modal
                .querySelector(".dish-details_price")
                ?.textContent.slice(0, -2)
                .replace(",", ".")
            ),
            name: modalName,
            quantity: 1,
            img: modal.querySelector(".dish-img").getAttribute("src"),
            id: modal.dataset.id,
            grams: +modal
              .querySelector(".dish-details_sizes")
              .textContent.split(" ")[0]
              .slice(0, -2),
          },
        ];
        modalQuantityEl.textContent = document
          .getElementById(modal.dataset.id)
          .querySelector(".item-quantity").textContent = 1;
      }

      renderCartItems();
    };

    document.querySelector("#item-buy .minus-btn").onclick = (e) => {
      const modal = document.querySelector("#item-buy");
      const modalName = modal.querySelector(".modal-title").textContent;
      const modalQuantityEl = modal.querySelector(".item-quantity");

      cart = cart.map((ci) => {
        if (ci.name === modalName) {
          console.log(ci);
          if (ci.quantity === 0) {
            return ci;
          }
          ci.quantity -= 1;
          const quantityEl = document
            .getElementById(ci.id)
            .querySelector(".item-quantity");
          quantityEl.textContent = modalQuantityEl.textContent = ci.quantity;
        }
        return ci;
      });
      renderCartItems();
    };
  });

  function handleClickOnMinus(e) {
    e.stopPropagation();

    const parentNode = e.target.parentNode;
    const quantity = parentNode.querySelector(".item-quantity").innerText;
    const productCard = e.target.parentNode.parentNode.parentNode;

    if (productCard.id === "order-data") {
      if (parseInt(quantity) === 1 || peopleQuantity === 1) return;
      const quantityEl = parentNode.querySelector(".item-quantity");
      peopleQuantity -= 1;
      quantityEl.innerText = peopleQuantity;
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
    if (productCard.id === "order-data") {
      const quantityEl = parentNode.querySelector(".item-quantity");
      peopleQuantity += 1;
      quantityEl.innerText = peopleQuantity;
      // setPrice();
      return;
    }
    if (menuItemPrice) price -= menuItemPrice;
    // setPrice();
    renderCartItems();
    // document.querySelector('.cart-full.pb-sm-4.mb-4').innerHTML=
  }

  function cleanCart() {
    cart = cart.filter((el) => el.quantity !== 0);
  }

  function handleClickOnPlus(e) {
    e.stopPropagation();
    const parentNode = e.target.parentNode;
    const productCard = e.target.parentNode.parentNode.parentNode;

    const menuItemPrice = getPrice(parentNode);
    if (productCard.id === "order-data") {
      const quantityEl = parentNode.querySelector(".item-quantity");
      peopleQuantity += 1;
      quantityEl.innerText = peopleQuantity;
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
          grams: +productCard
            .querySelector(".dish-details_sizes")
            .textContent.slice(0, -2),
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
