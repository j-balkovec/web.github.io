let num1 = "";
let num2 = "";
let operator = "";
let display = document.getElementById("display");
let currentNumber = "";
let result = "";

function addNumber(number) {
    if (result) {
      currentNumber = number;
      result = "";
    } else {
      currentNumber += number;
    }
    display.textContent = currentNumber;
  }
  
  function addDecimal() {
    if (!currentNumber.includes(".")) {
      currentNumber += ".";
    }
    display.textContent = currentNumber;
  }
  
  function changeSign() {
    if (currentNumber) {
      currentNumber *= -1;
      display.textContent = currentNumber;
    } else if (result) {
      result *= -1;
      display.textContent = result;
    }
  }
  
  function backspace() {
    if (currentNumber) {
      currentNumber = currentNumber.slice(0, -1);
      display.textContent = currentNumber;
    }
  }
  
  function clear() {
    num1 = "";
    num2 = "";
    operator = "";
    currentNumber = "";
    result = "";
    display.textContent = "0";
  }
  
  function operate(op) {
    if (currentNumber && operator) {
      calculate();
    }
    operator = op;
    num1 = currentNumber;
    currentNumber = "";
  }
  
  function calculate() {
    num2 = currentNumber;
    currentNumber = "";
  
    switch (operator) {
      case "+":
        result = parseFloat(num1) + parseFloat(num2);
        break;
      case "-":
        result = parseFloat(num1) - parseFloat(num2);
        break;
      case "*":
        result = parseFloat(num1) * parseFloat(num2);
        break;
      case "/":
        result = parseFloat(num1) / parseFloat(num2);
        break;
      default:
        return;
    }
  
    if (result.toString().length > 10) {
      result = result.toExponential(5);
    }
  
    display.textContent = result;
  }
  