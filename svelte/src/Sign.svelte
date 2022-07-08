<script>
  import {ModalHiddenEventListener} from "./utils";
  import {request, signIn, signUp} from "./api";
  import {correctPhoneWithMask} from "./helpers/correctPhoneWithMask";
  import {captchaProtect} from "./helpers/grecaptcha";
  import CodeInput from "./components/CodeInput.svelte";

  let phone = "",
          password = "", recoverPhone = '';
  let isRegisteredNumber = false
  let isDeletedAccount = false
  let code = ["", "", "", ""];

  let ui = {
    showMainModal: false,
    showSignInModal: false,
    showSignUpModal: false,
    showRecoveryModal: false
  };

  let errors = {
    recoveryCodeError: false,
    recoveryPhoneError: false,
    signInPhoneError: false,
    signInPasswordError: false,
    signInError: false,
    userDeletedError: false
  }

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSignInSubmit(e) {
    e.preventDefault();
    if(!correctPhoneWithMask(phone) || !password.trim()) {
      if(!correctPhoneWithMask(phone)){
        errors.signInPhoneError = true
        setTimeout(() => {
          errors.signInPhoneError = false
        }, 3000)
      }
      if(!password.trim()){
        errors.signInPasswordError = true
        setTimeout(() => {
          errors.signInPasswordError = false
        }, 3000)
      }
      return
    }
    // grecaptcha.ready(function () {
    //     grecaptcha.execute(recaptchaKey, {action: 'submit'}).then(async function(token) {
    //         const captchaResponse = await request('POST', '/captcha', {token})
    //         console.log({captchaResponse})
    //         if(!captchaResponse.success) {
    //             return
    //         }
    //         const signInResponse = await signIn({phone, password});
    //         if (signInResponse.success) {
    //             window.location.href = "/personal";
    //         } else {
    //             errors.signInError = true
    //             setTimeout(() => {errors.signInError = false}, 3000)
    //         }
    //     });
    // });
    captchaProtect(async () => {
      const signInResponse = await signIn({phone, password});
      if (signInResponse.success) {
        if (signInResponse.is_staff){
          window.location.href = "/pcpanel";
        }
        window.location.href = "/personal";
      } else {
        if (signInResponse.error_code == 1) {
          errors.userDeletedError = true;
          setTimeout(() => {errors.userDeletedError = false}, 3000)
        } else {
          errors.signInError = true
          setTimeout(() => {errors.signInError = false}, 3000)
        }
      }
    })

  }

  function handleRecoverSubmit(e) {
    e.preventDefault()
    ui.showMainModal = false
    ui.showSignInModal = false
    ui.showSignUpModal = false
    ui.showMainModal = false
    hideModals();
    ui.showRecoveryModal = true
    showModal('forgot-password')
  }

  function handleGetCode(e) {
console.log({recoverPhone})
    e.preventDefault()
    if (!correctPhoneWithMask(recoverPhone)) return
    captchaProtect(async () => {
      const response = await request('POST', '/recovery', {phone: recoverPhone})
      if(response.error){
        errors.recoveryPhoneError = true
        setTimeout(() => {
          errors.recoveryPhoneError = false
        }, 3000)
        return
      }
      document.querySelector('.send-reset').click()
    })

  }


  async function handleSubmitRecover(e) {
    e.preventDefault()
    const password = code.join('')
    if (password.length !== 4) return
    const response = await request('POST', '/signin', {phone: recoverPhone, password})
    if (response.success) {
      ui.showRecoveryModal = false;
      if (response.is_staff) {
        window.location.href = '/pcpanel';
      }
      window.location.href = '/personal';
    } else {
      errors.recoveryCodeError = true
      setTimeout(() => {
        errors.recoveryCodeError = false
      }, 3000)
    }
  }

  async function handleSignUpSubmit(e) {
    e.preventDefault();
    captchaProtect(async () => {
      const response = await signUp({phone});
      console.log(response);
      if (response.success) {
        // console.log('gi')
        // code = response.password.split("");
        document.querySelector('.send-register').click()
      } else {
        console.log({deletedAcc: "Maybe acc is deleted"})
        if (response.error_code == 1) {
          console.log({deletedAcc: "Account is deleted"})
          isDeletedAccount = true;
        } else {
          console.log({deletedAcc: "Account is registered"})
          isRegisteredNumber = true;
        }
      }
    })

  }

  document.addEventListener("DOMContentLoaded", () => {
    const signBtns = document.querySelectorAll(".sign");
    if (signBtns.length > 0) {
      signBtns.forEach((e) =>
              e.addEventListener("click", () => {
                ui.showMainModal = true;
                document
                        .querySelectorAll(".modal")
                        .forEach((elem) => (elem.style.display = ""));
              })
      );
    }

    ModalHiddenEventListener(
            document.querySelector("#signinup"),
            (e) => {
              ui.showMainModal = false;
            },
            document
    );

    ModalHiddenEventListener(
            document.querySelector("#login"),
            () => {
              ui.showSignInModal = false;
            },
            document
    );

    ModalHiddenEventListener(
            document.querySelector("#register"),
            () => {
              ui.showSignUpModal = false;
            },
            document
    );

    if (window.location.hash == '#login') {
      document.querySelector("html").classList.add("locked");
      document.querySelector("body").classList.add("locked");
      const toLoginBtn = document.querySelector('#signinup a.submit');
      toLoginBtn.dispatchEvent(new Event('click'));
    }

    // document.querySelector('#signinup').addEventListener("hidden.bs.modal", () => {
    //   alert("AA")
    //   ui.showMainModal = false;
    // });

    // document.querySelector('#login').addEventListener("hide.bs.modal", () => {
    //   ui.showSignInModal = false;
    // })

    // document.querySelector('#register').addEventListener("hide.bs.modal", () => {
    //   ui.showSignUpModal = false;
    // })
  });

  function hideModals() {
    [...document.getElementById("sign-target").children].forEach((el) => {
      el.style.display = "none";
      el.classList.remove("show");
    });
  }

  function showModal(id) {
    const modal = document.getElementById(id)
    modal.style.display = "";
    modal.classList.add("show");
  }
</script>

<!-- MAIN MODAL -->
<div
  class="modal modal-wrapper fade {ui.showMainModal ? 'show' : ''}"
  id="signinup"
  tabindex="-1"
  role="dialog"
>
  <div class="modal-dialog" style="max-width: 424px">
    <div class="modal-content">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
        on:click={() => {
          ui.showMainModal = false;
        }}
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-header mt-3 mt-sm-0">
        <div class="modal-title">Личный кабинет</div>
      </div>
      <div class="pb-3">
        <!-- svelte-ignore a11y-missing-attribute -->
        <a
          class="mt-0 mb-3 submit d-block text-center"
          on:click={() => {
            ui.showMainModal = false;
            ui.showSignInModal = true;
            showModal('login')
          }}>Войти</a
        >
        <!-- svelte-ignore a11y-missing-attribute -->
        <a
          class="download active d-block text-center"
          on:click={() => {
            ui.showMainModal = false;
            ui.showSignUpModal = true;
            hideModals();
            showModal("register");
            isRegisteredNumber = false
            isDeletedAccount = false
          }}>Зарегистрироваться</a
        >
      </div>
    </div>
  </div>
</div>

<!-- ENTER MODAL -->

<div
  class="modal modal-wrapper fade {ui.showSignInModal ? 'show' : ''}"
  id="login"
  tabindex="-1"
  role="dialog"
>
  <div class="modal-dialog" style="max-width: 492px">
    <div class="modal-content">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
        on:click={() => {
          ui.showSignInModal = false;
        }}
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-header"><div class="modal-title">Вход</div></div>
      <form on:submit={handleSignInSubmit} preventDefault={validate}>
        {#if errors.signInError}
          <h3 class="text-center" style="color: red;">Неверные данные</h3>
        {/if}
        {#if errors.userDeletedError}
          <h3 class="text-center" style="color: red;">Пользователь с таким телефоном был удалён</h3>
        {/if}
        <input
          class="login-input {errors.signInPhoneError && 'error-shadow'}"
          name="phone"
          bind:value={phone}
          on:change={e => phone = e.target.value}
          placeholder="Телефон"
        />
        <input
          class="password-input {errors.signInPasswordError && 'error-shadow'}"
          type="password"
          name="password"
          bind:value={password}
          placeholder="Пароль"
        />
        <div class="text-center">
          <a class="submit" href="#" on:click={handleSignInSubmit}>Войти</a>
        </div>
      </form>
      <div class="modal-description text-center mt-4">
        <a href="#forgot-password" data-modal>Забыли пароль?</a>
      </div>
    </div>
  </div>
</div>

<!-- Forgot password MODAL -->
<div
        class="modal-wrapper modal fade {ui.showRecoveryModal ? 'show' : ''}"
        id="forgot-password"
        tabindex="-1"
        role="dialog"
>
  <div class="modal-dialog" style="max-width: 492px">
    <div class="modal-content cart-top">
      <div class="modal-header">
        <button
                class="close"
                type="button"
                data-dismiss="modal"
                aria-label="Close"
        >
          <span aria-hidden="true">&times;</span>
        </button>
        <div class="modal-title">Забыли пароль?</div>
      </div>
      <div class="stages">
        <form class="stage" action="">
          <div class="modal-description">Введите Ваш номер телефона</div>
          {#if errors.recoveryPhoneError}
            <p class="text-center" style="color: red;font-size: 17px; letter-spacing: .7px;">На этот телефон не зарегистрирован аккаунт!</p>
          {/if}
          <input
                  class="phone-input"
                  name="phone"
                  placeholder="Ваш телефон"
                  bind:value={recoverPhone}
                  on:change={e => recoverPhone = e.target.value}
          />
          <div class="text-center">
            <a class="send-reset d-none" href="#"></a>
            <a class="submit" href="#" on:click={handleGetCode}>Получить код</a>
          </div>
        </form>
        <form class="stage" action="">
          {#if errors.recoveryCodeError}
            <h3 class="text-center" style="color: red;">Неправильный код</h3>
          {/if}
          <div class="modal-description">Введите код из СМС</div>
          <div class="d-flex justify-content-between code-inputs">
            <CodeInput bind:value="{code[0]}"/>
            <CodeInput bind:value="{code[1]}"/>
            <CodeInput bind:value="{code[2]}"/>
            <CodeInput bind:value="{code[3]}"/>
          </div>
          <div class="text-center">
            <a class="submit reset-password" on:click={handleSubmitRecover} href="#">
              Войти
            </a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- REGISTRATION MODAL -->
<div
  class="modal-wrapper modal fade {ui.showSignUpModal ? 'show' : ''}"
  id="register"
  tabindex="-1"
  role="dialog"
>
  <div class="modal-content" style="max-width: 492px">
    <div class="modal-header">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
        on:click={() => {
          ui.showSignUpModal = false;
        }}
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-title">Регистрация</div>
    </div>
    <div class="stages">
      {#if (!isRegisteredNumber)}
        <form class="stage" action="">
          <div class="modal-description">Введите Ваш номер телефона</div>
          <input
                  class="phone-input"
                  type="tel"
                  name="phone"
                  on:change={(e) => (phone = e.target.value)}
                  placeholder="Ваш телефон"
          />
          <div class="text-center">
            <a class="send-register d-none" href="#"></a>
            <a class="submit" on:click={handleSignUpSubmit} href="#"
            >Получить код</a
            >
          </div>
        </form>
      {:else}
        <div class="text-center">
          <h3>Этот номер зарегистрирован!</h3>
        </div>
      {/if}
      <form class="stage" action="">
        <div class="modal-description">Введите код из СМС</div>
        {#if errors.signInError}
          <h3 class="text-center" style="color: red;">Неверные данные</h3>
        {/if}
        <div class="d-flex justify-content-between code-inputs">
          <CodeInput bind:value="{code[0]}"/>
          <CodeInput bind:value="{code[1]}"/>
          <CodeInput bind:value="{code[2]}"/>
          <CodeInput bind:value="{code[3]}"/>
        </div>
        <div class="text-center">
          <!-- svelte-ignore a11y-missing-attribute -->
          <a
            class="submit verify-registration"
            on:click={(e) => {
              password = code.join("");
              handleSignInSubmit(e);
            }}>Зарегистрироваться</a
          >
        </div>
      </form>
    </div>
  </div>
</div>

<style>
  .modal-dialog {
    z-index: 9999;
  }
</style>
