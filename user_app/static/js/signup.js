const form = document.getElementById('form');
const submitBtn = document.getElementById('submit');
const submitDiv = document.querySelector(".submit")
const inputsDiv = document.querySelector(".inputs")


let preventedOnce = false;

let login, first_name, surname, email, password

form.addEventListener('submit', (e) => {
    if (!preventedOnce) {
        e.preventDefault();
        preventedOnce = true;

        login = document.getElementById("login").value.trim();
        first_name = document.getElementById("name").value.trim();
        surname = document.getElementById("surname").value.trim();
        email = document.getElementById("email").value.trim();
        password = document.getElementById("password").value;

        validate({ login, first_name, surname, email, password });
    }
    else {
        e.preventDefault();
        const inputs = document.querySelectorAll(".input-code-number");
        const code = Array.from(inputs).map(input => input.value.trim()).join("");
        fetch("/validate-code/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            login,
            first_name,
            surname,
            email,
            password,
            code
        })
        })
        .then(res => res.json())
        .then(result => {
            if (result.success) {
                window.location.href = window.location.origin + result.url
            } else {
                alert("❌ Код Невірний!");
            }
        })
        .catch(err => console.error("Ошибка:", err));
    }
});

function validate(data) {
    fetch("/validate/", {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            form.style.height = "270px"; 
            submitDiv.remove();
            inputsDiv.remove();
            const img = document.createElement("img")
            img.src = "/user/images/wait.svg"
            img.id = "waitImg"
            form.appendChild(img)
            fetch("/sendcode/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(result => {
                setTimeout(()=>{
                    const subtitle = document.createElement('h3')
                    subtitle.classList.add("subtitle")
                    subtitle.textContent = "Майже готово!"
                    const desc = document.createElement('p')
                    desc.classList.add("desc")
                    desc.textContent = `Ми надіслали код підтвердження на вашу пошту (${email}).\nВведіть його нижче, щоб продовжити.`
                    const helpText = document.createElement('p')
                    helpText.classList.add("help-text")
                    helpText.textContent = 'Не отримали код? Відправити ще раз'
                    
                    const divInputs = document.createElement("div")
                    divInputs.classList.add("code-div")
                    // 
                    const inputNumber1 = document.createElement('input')
                    inputNumber1.classList.add('input-code-number')
                    inputNumber1.maxLength = 1
                    divInputs.appendChild(inputNumber1)
    
                    const inputNumber2 = document.createElement('input')
                    inputNumber2.classList.add('input-code-number')
                    inputNumber2.maxLength = 1
                    divInputs.appendChild(inputNumber2)
                    
                    const inputNumber3 = document.createElement('input')
                    inputNumber3.classList.add('input-code-number')
                    inputNumber3.maxLength = 1
                    divInputs.appendChild(inputNumber3)
                    
                    const inputNumber4 = document.createElement('input')
                    inputNumber4.classList.add('input-code-number')
                    inputNumber4.maxLength = 1
                    divInputs.appendChild(inputNumber4)
                    
                    const inputNumber5 = document.createElement('input')
                    inputNumber5.classList.add('input-code-number')
                    inputNumber5.maxLength = 1
                    divInputs.appendChild(inputNumber5)
                    
                    const inputNumber6 = document.createElement('input')
                    inputNumber6.classList.add('input-code-number')
                    inputNumber6.maxLength = 1
                    divInputs.appendChild(inputNumber6)
                    // 
                    const submitDivvv = document.createElement("div")
                    submitDivvv.classList.add("submit")
                    
                    const buttonSubmit = document.createElement('button')
                    buttonSubmit.id = 'submit'
                    buttonSubmit.textContent = "Підтвердити"
                    submitDivvv.appendChild(buttonSubmit)
                    img.remove();
                    form.style.height = "485px"; 
                    form.appendChild(subtitle)
                    form.appendChild(desc)
                    form.appendChild(divInputs)
                    form.appendChild(helpText)
                    form.appendChild(submitDivvv)
                }, 1000)
            })
        } else {    

            alert("❌ " + result.message);
            preventedOnce = false; 
        }
    })
    .catch(err => {
        console.error("Помилка запроса:", err);
        preventedOnce = false;
    });
}
