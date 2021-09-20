<script>
  import { ModalHiddenEventListener } from "./utils";
  import { signIn, signUp } from "./api";

  let phone = "",
    password = "";

  let code = ["", "", "", ""];

  let ui = {
    showMainModal: false,
    showSignInModal: false,
    showSignUpModal: false,
  };

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSignInSubmit(e) {
    e.preventDefault();
    const response = await signIn({ phone, password });
    if (response.success) {
      window.location.href = "/personal";
    }
  }

  async function handleSignUpSubmit(e) {
    e.preventDefault();
    const response = await signUp({ phone });
    console.log(response);
    if (response.success) {
      code = response.password.split("");
    }
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
            ui.showMainModal = !ui.showMainModal;
            ui.showSignInModal = !ui.showSignInModal;
          }}>Войти</a
        >
        <!-- svelte-ignore a11y-missing-attribute -->
        <a
          class="download active d-block text-center"
          on:click={() => {
            ui.showMainModal = !ui.showMainModal;
            ui.showSignUpModal = !ui.showSignUpModal;
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
        <input
          class="login-input"
          name="phone"
          bind:value={phone}
          placeholder="Телефон"
        />
        <input
          class="password-input"
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
      <form class="stage" action="">
        <div class="modal-description">Введите Ваш номер телефона</div>
        <input
          class="phone-input"
          type="tel"
          name="phone"
          bind:value={phone}
          placeholder="Ваш телефон"
        />
        <div class="text-center">
          <a class="submit send-register" on:click={handleSignUpSubmit} href="#"
            >Получить код</a
          >
        </div>
      </form>

      <form class="stage" action="">
        <div class="modal-description">Введите код из СМС</div>
        <div class="d-flex justify-content-between code-inputs">
          <input
            class="code-input"
            type="number"
            name="code1"
            bind:value={code[0]}
            max="9"
            min="0"
            step="1"
          />
          <input
            class="code-input"
            type="number"
            name="code2"
            bind:value={code[1]}
            max="9"
            min="0"
            step="1"
          />
          <input
            class="code-input"
            type="number"
            name="code3"
            bind:value={code[2]}
            max="9"
            min="0"
            step="1"
          />
          <input
            class="code-input"
            type="number"
            name="code4"
            bind:value={code[3]}
            max="9"
            min="0"
            step="1"
          />
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
