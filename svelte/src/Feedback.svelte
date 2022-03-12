<script>
  import { feedbackRequest } from "./api";
  import {correctPhoneWithMask} from "./helpers/correctPhoneWithMask";
  import {captchaProtect} from "./helpers/grecaptcha";

  let name = "";
  let phone = "";
  let description = "";
  let errors = {}

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    console.log(correctPhoneWithMask(phone))
    console.log('ERRORS HANDLING TESST')
    if(!correctPhoneWithMask(phone) || !description) {
      console.log('ERRORS HANDLING TESST2')
      errors.phone = !correctPhoneWithMask(phone)
      errors.description = !description
      setTimeout(() => {
        errors = {}
      }, 3000)
      return
    }
    captchaProtect(async () => {
      const response = await feedbackRequest({ name, phone, description });
      document.querySelector('.send-feedback').click()
      console.log(response);
      description = name = phone = ''
    })
  }
</script>

<div class="modal-wrapper modal fade" id="feedback" tabindex="-1" role="dialog">
  <div class="modal-dialog" style="max-width: 659px">
    <div class="modal-content">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-header">
        <div class="modal-title">Оставьте свой отзыв</div>
        <div class="modal-title success">Ваш отзыв успешно отправлен</div>
      </div>
      <div class="modal-description black">
        С нетерпением ждем ваших замечаний, пожеланий, предложений!
      </div>
      <form action="" on:submit={handleSubmit} preventDefault={validate}>
        <input name="name" placeholder="Ваше имя" bind:value={name} />
        <input
          class="phone-input {errors.phone && 'error-shadow'}"
          type="tel"
          name="phone"
          placeholder="Ваш телефон"
          on:change={(e) => phone = e.target.value }
          value={phone}
        />
        <textarea
          class="{errors.description && 'error-shadow'}"
          name="description"
          placeholder="Напишите свой отзыв..."
          rows="4"
          bind:value={description}
        />
        <div class="text-center" style="margin-top: 20px">
          <a href="#" class="d-none send-feedback"></a>
          <a href="#" class="submit" on:click={handleSubmit}
            >Отправить отзыв</a
          >
          <!-- <a href="#" class="submit send-feedback" on:click={handleSubmit}>Отправить отзыв</a> -->
        </div>
      </form>
    </div>
  </div>
</div>
