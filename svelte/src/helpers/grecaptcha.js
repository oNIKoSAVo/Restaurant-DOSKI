import {request, signIn} from "../api";

export async function captchaProtect(fn){
    grecaptcha.ready(function () {
        grecaptcha.execute('6Ldt-3IdAAAAANmg-3m44sDmGtdYTyC_ZNH-CbO8', {action: 'submit'}).then(async function(token) {
            const captchaResponse = await request('POST', '/captcha', {token})
            console.log({captchaResponse})
            if(!captchaResponse.success) {
                return
            }
            fn()
        });
    });
}
