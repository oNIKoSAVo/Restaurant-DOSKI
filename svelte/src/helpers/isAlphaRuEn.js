import isAlpha from "validator/es/lib/isAlpha";

export default function isAlphaRuEn(str){
    return isAlpha(str, "ru-RU", { ignore: "s" }) || isAlpha(str, "en-US", { ignore: "s" })
}
