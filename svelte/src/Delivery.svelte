<script>
    import {cloneDeep, isEqual} from "lodash-es";
    import {correctPhoneWithMask} from "./helpers/correctPhoneWithMask";
    import jquery from "jquery";
    import {sendTelegramMessage} from "./helpers/sendTelegramMessage";
    import {setErrorShadow} from "./helpers/setErrors";
    import dayjs from "dayjs";
    import isBetween from 'dayjs/plugin/isBetween'
    import utc from 'dayjs/plugin/utc';
    import timezone from 'dayjs/plugin/timezone';


    dayjs.extend(isBetween)
    dayjs.extend(utc)
    dayjs.extend(timezone)

    let currentCityChanged = false;
    let managerSettingsGetted = false;

    $: if (currentCityChanged && managerSettingsGetted) {
        console.log('disabling btn');
        const allow_weekday_time_delivery = {
            start: window.managerSettings['allow_time_delivery_start'],
            end: window.managerSettings['allow_time_delivery_end']
        }
        
        const allow_delivery_hour_start = parseInt(allow_weekday_time_delivery.start);
        const allow_delivery_hour_end = parseInt(allow_weekday_time_delivery.end);

        const delivery_timef_el = document.getElementById('delivery-time_from');
        const delivery_timet_el = document.getElementById('delivery-time_to');
        if (delivery_timef_el && delivery_timet_el) {
            delivery_timef_el.textContent = allow_delivery_hour_start + '-00';
            delivery_timet_el.textContent = allow_delivery_hour_end + '-00';
    
            const submitEl = document.querySelector('#cart .submit');
            
            disable_btn_ontime(submitEl, 
                               allow_delivery_hour_start, 
                               allow_delivery_hour_end);
        }
    }

    let cart = [];
    $: price = cart.reduce(
        (acc, cartItem) => acc + cartItem.price * cartItem.quantity,
        0
    );
    $: grams = cart.filter(cartItem => cartItem.grams).reduce(
        (acc, cartItem) => acc + cartItem.grams * cartItem.quantity,
        0
    );
    $: milliliters = cart.filter(cartItem => cartItem.milliliters).reduce(
        (acc, cartItem) => acc + cartItem.milliliters * cartItem.quantity,
        0
    );
    $: setPrice(price, grams, milliliters);
    let peopleQuantity = 1;
    // $: priceWithQuantity = price * peopleQuantity;
    // $: console.log(priceWithQuantity);
    $: console.log({cart});
    window.renderCartItems = renderCartItems;

    // $: document.querySelector(".cart-summary").textContent = price;

    function switchStage(modalSelectorStr, stage) {
        [...document.querySelectorAll(`${modalSelectorStr} .stage`)].map((s, i) => {
            if (i === stage-1) {
                s.style = "display: block;";
            } else {
                s.style = "display: none;";
            }
            return s;
        });
    }

    function openModal(id) {
        jquery(".modal").removeClass("show").hide();
        // saveTop = jquery("html").scrollTop();
        // jquery(".modal-title").text(title);
        // jquery(".modal-subtitle").text(subtitle);
        jquery("html,body").addClass("locked");
        jquery("body").css("overflow", "hidden");
        // jquery("body").css("top", -saveTop);
        document.querySelector(id).style.display = "";
        jquery(id).addClass("show").show();
    }
    
    function disable_btn_ontime(btn, time_start, time_end) {
        console.log(window.currentCity.city_timezone);
        let currentTimeInCity = dayjs().tz(window.currentCity.city_timezone);
        console.log({ctc: currentTimeInCity.hour(), start: time_start, end: time_end});
        let current_hour = currentTimeInCity.hour();
        
        if (!(current_hour >= time_start && current_hour < time_end)) {
            console.log('add disabled')
            btn.classList.add('disabled');
        } else {
            console.log('remove disabled')
            btn.classList.remove('disabled');
        }
    }

    window.addEventListener('currentCityChange', ()=>{
        currentCityChanged = true;
        console.log('currentCityChange');
    });

    window.addEventListener('managerSettingsGet', () => {
        managerSettingsGetted = true;
        console.log('managerSettingsGEt');
    });

    function isDrink(gramsStr) {
        return gramsStr.slice(-2) !== 'гр';
    }

    function getWeight(gramsStr) {
        console.log({gramsStr: gramsStr.slice(0, -2)})
        const gramsArr = gramsStr.slice(0, -2).split('/')
        return gramsArr.reduce((acc, grams) => acc += +grams, 0)
    }

    function renderCartItems() {
        cleanCart();
        console.log(cart.length);
        // if (cart.length === 0) {
        //   document.querySelector(
        //     ".cart-full.pb-sm-4.mb-4"
        //   ).innerHTML = `<h1>Пусто</h1>`;
        //   return;
        // }
        // [...document.querySelectorAll("#cart .stage")].map((s, i) => {
        //     if (i === 0) {
        //         s.style = "display: block;";
        //     } else {
        //         s.style = "display: none;";
        //     }
        //     return s;
        // });
        switchStage("#cart", 1);

        let cartHtml;
        console.log(cart.length > 0);
        if (cart.length > 0) {
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
              <div class="cart-item_price text-right">${cartItem.price * cartItem.quantity}Р</div>
          </div>`;
                })
                .join("");
        } else {
            cartHtml = "<h1>Корзина пуста</h1>";
        }

        document
            .querySelectorAll(".cart-full")
            .forEach((el) => (el.innerHTML = cartHtml));

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
                    const priceElInCart = cartItem.querySelector(".cart-item_price");
                    cart = cart.map((ci) => {
                        if (ci.name === cartName) {
                            ci.quantity += 1;
                            priceElInCart.textContent = ci.quantity * ci.price;
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
                        const priceElInCart = cartItem.querySelector(".cart-item_price");
                        const lastCart = [...cart];

                        cart = cart.map((ci) => {
                            if (ci.name === cartName && ci.quantity !== 0) {
                                ci.quantity -= 1;
                                priceElInCart.textContent = ci.quantity * ci.price;
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

    function cleanCart() {
        cart = cart.filter((el) => el.quantity !== 0);
    }

    function getPrice(parentNode) {
        try {
            return Number(
                parentNode.parentNode
                    .querySelector(".dish-details_price")
                    ?.textContent.slice(0, -1)
                // .replace(",", ".")
            );
        } catch (err) {
        }
    }

    function setPrice() {
        try {
            // document.querySelector(".cart-summary").textContent =
            //   document.querySelector(".cart-summary_amount.text-right").textContent =
            //     price + ".-";
            //   console.log({cs: document.querySelector(".cart-summary_amount.text-right")})
            setTimeout(() => {
                const totalPrice = document.querySelectorAll(".cart-summary")
                const cartSummaryPrice = document.querySelectorAll(".cart-summary_amount")
                if (!totalPrice || !cartSummaryPrice) return
                [...totalPrice, ...cartSummaryPrice].forEach(el => el.textContent = price + "Р")
                // totalPrice.textContent = cartSummaryPrice.textContent = price + "Р";
                console.log({cs: document.querySelector(".cart-summary_amount.text-right")})
                if (document.querySelector('.gram b') && document.querySelector('.milliliter b')) {
                    document.querySelector('.gram b').textContent = `${Math.round(grams / peopleQuantity)}гр`
                    document.querySelector('.milliliter b').textContent = `${Math.round(milliliters / peopleQuantity)}мл`
                }
            }, 0);
        } catch (err) {
            console.error(err)
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
    let lastCartSent = cloneDeep(cart)
    let lastPreorderDownloadHref = ``

    async function downloadPreorder() {
        const preorderResponse = await fetch('/preorder', {
            body: JSON.stringify({
                menue: cart,
                restaraunt: 1,
                comment: 'Предзаказ',
                reservation: ''
            }), headers: {'Content-Type': 'application/json'}, method: 'POST'
        })
        const preorderResponseJson = await preorderResponse.json()
        // const downloadResponse = await fetch(`/download_preorder?id=${preorderResponseJson.id}`)
        lastPreorderDownloadHref = `/download_preorder?id=${preorderResponseJson.id}`
        window.location.href = lastPreorderDownloadHref
    }

    document.addEventListener("DOMContentLoaded", () => {
        if (!localStorage.getItem("currentAddress")) {
            openModal("#checkAddress");
        }

        const [downloadBtn, printBtn, shareBtn] = [...document.querySelector('.preorder-buttons').children]
        downloadBtn.addEventListener('click', () => {
            if (cart.length === 0 || isEqual(cart, lastCartSent)) {
                window.location.href = lastPreorderDownloadHref
                return
            }
            lastCartSent = cloneDeep(cart)
            downloadPreorder()
        })
        document
            .querySelector(".checkout-final-fake")
            .addEventListener("click", async (e) => {
                console.log('was here')
                const currentStage = e.target.closest(".stage");
                const nameInputEl = currentStage.querySelector('input[name="name"]');
                const addressInputEl = currentStage.querySelector('input[name="addres"]');
                const phoneInputEl = currentStage.querySelector('input[name="phone"]');
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
                const paymentTypeSelectEl = document
                    .querySelector("#checkoutform select[name='paymentType']")
                let paymentType = paymentTypeSelectEl.value.trim();

                if (currentStage) {
                    if (
                        fio === "" ||
                        address === "" ||
                        phone === "" ||
                        paymentType === '' ||
                        !correctPhoneWithMask(phone)
                    ) {
                        if (fio === "") setErrorShadow(nameInputEl);
                        if (address === "") setErrorShadow(addressInputEl);
                        if (paymentType === "") setErrorShadow(paymentTypeSelectEl);
                        if (
                            !correctPhoneWithMask(phone)
                        )
                            setErrorShadow(phoneInputEl);
                        return;
                    }
                }
                if(paymentType === 'Банковская карта'){
                    paymentType = 1
                }
                else if (paymentType === 'Онлайн оплата'){
                    paymentType = 0
                }
                else if(paymentType==='Наличные'){
                    paymentType = 2
                }
                // обработка заказа
                // const checkoutData = $("#checkoutform").serializeArray();

                // Успешный исход

                if (!fio || !address || !correctPhoneWithMask(phone)) return;
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
                    const cartItemsTitlesWithQuantity = [
                        ...document.querySelector(".cart-full").querySelectorAll(".cart-item"),
                    ].map(
                        (el) =>
                            `${el.querySelector(".cart-item_title").textContent} * ${
                                el.querySelector(".item-quantity").textContent
                            }`
                    );
                    sendTelegramMessage(
                        `${fio} заказал доставку на адрес "${address}". Блюда: ${cartItemsTitlesWithQuantity.join(
                            ", "
                        )}. Номер: ${phone}. Цена заказа: ${
                            document.querySelector(".cart-summary").textContent
                        }.`
                    );
                    document.querySelector('.checkout-final').click()
                    window.location.href = result.payment_url;
                } else if (result.status_code == 401) {
                    console.log('Mb need to close modal');
                    console.log(result.message);
                    // const orderFinalEl = document.getElementById("order-final-modal")

                    openModal("#order-final-modal", 1);
                    switchStage("#cart", 1);
                } else {
                    console.log(result);
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
                const gramsStr = modal.querySelector('.dish-details_sizes').textContent
                cart = [
                    ...cart,
                    {
                        price: Number(
                            modal
                                .querySelector(".dish-details_price")
                                ?.textContent.slice(0, -1)
                                .replace(",", ".")
                        ),
                        name: modalName,
                        quantity: 1,
                        img: modal.querySelector(".dish-img").getAttribute("src"),
                        id: modal.dataset.id,
                        [isDrink(gramsStr) ? 'milliliters' : 'grams']: getWeight(gramsStr)
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
        const productCard = e.target.closest('.dish-item');
        console.log({productCard})
        if (!productCard) {
            if (parseInt(quantity) === 1 || peopleQuantity === 1) return;

            const quantityEl = parentNode.querySelector(".item-quantity");
            peopleQuantity -= 1;
            quantityEl.innerText = peopleQuantity;
            setPrice();
            return;
        }

        if (parseInt(quantity) === 0) return;

        const productIndex = cart.findIndex((el) => {
            console.log({productCard})
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
        e.stopPropagation();
        const parentNode = e.target.parentNode;
        const productCard = e.target.closest('.dish-item');

        console.log({productCard})

        const menuItemPrice = getPrice(parentNode);
        if (!productCard) {
            const quantityEl = parentNode.querySelector(".item-quantity");
            peopleQuantity += 1;
            quantityEl.innerText = peopleQuantity;
            setPrice();
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
            const gramsStr = productCard.querySelector('.dish-details_sizes').textContent
            cart = [
                ...cart,
                {
                    price: menuItemPrice,
                    name: productCard.querySelector(".dish-title").textContent,
                    quantity: 1,
                    img: productCard.querySelector(".dish-img").getAttribute("src"),
                    id: productCard.id,
                    [isDrink(gramsStr) ? 'milliliters' : 'grams']: getWeight(gramsStr)

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
