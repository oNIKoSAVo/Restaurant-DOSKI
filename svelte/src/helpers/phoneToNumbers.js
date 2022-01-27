export function phoneToNumbers(phoneString) {
  return (
    "8" +
    phoneString
      .slice(2)
      .split("")
      .filter((el) => {
        if (!isNaN(+el)) return true;
      })
      .join("")
  );
}

export function numbersToPhone(phoneNumbers){
    return phoneNumbers ? `+7(${phoneNumbers.slice(1, 4)})-${phoneNumbers.slice(4, 7)}-${phoneNumbers.slice(7, 9)}-${phoneNumbers.slice(9, 11)}` : null
}
