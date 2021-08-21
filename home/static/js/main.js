
// Clock
function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}
function getDatee() {
    let clock = document.querySelectorAll('.clock');
    let fullDate = document.querySelector('.fullDate');
    let d = new Date()
    clock.forEach((val, ind) => {
        val.innerHTML = `${addZero(d.getHours())}:${addZero(d.getMinutes())}`;
        fullDate.innerHTML = `${String(d)[0] + String(d)[1] + String(d)[2]} ${addZero(d.getHours())}:${addZero(d.getMinutes())}`;
    })
}

// getDatee()

// setInterval('getDatee()', 10000)
// =====================-  -=============================
function numberWithCommas(x) {return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ","); } 

$(function() {
    // mask
    $('.amount').mask("#,###,###",{reverse: true});
    $('.numMusk').mask("#,###,###",{reverse: true});

    var total_amount = function() {
        var sum;
        if ($('#id_outsidePrice').unmask().val() == undefined){
            var sum = $('#id_kg').val() * $('#id_price').unmask().val();
        } else {
            var sum = $('#id_kg').val() * $('#id_outsidePrice').unmask().val();
        }
        $("#id_totalSum").val(numberWithCommas(sum));
        // $("#id_totalSum").mask("#,###",{reverse: true});
    }
    $('.amount').on('input', function() {
        total_amount()
        $('.amount').mask("#,###",{reverse: true});
    })
})
function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

// for takeMoney
try {
    addMoneyWhenTakeMoneyBtn.onclick = function() {
        if (id_TakeMoney.value.includes(',')) {
            $('.amount').unmask()
        }
        addMoneyWhenTakeMoneyId.submit()
        id_TakeMoney.value = '';
    }
} catch {
    //
}

try {
    subBtn.onclick = function() {
        if (id_kg.value.includes(',')) {
            // $('.amount').unmask()
            // $('.amount').unmask()
        } if (id_totalSum.value.includes(',')) {
            $('.amount').unmask()
        } if (window.location.pathname == "/savdo/") {
            
        }
        try {
            if (id_outsidePrice.value.includes(',')) {
                $('.amount').unmask()
            }
            if (isNumber(id_kg.value) && isNumber(id_outsidePrice.value)) {
                enterForm.submit();
                id_kg.value = '';
                id_outsidePrice.value = '';
            } else
                alert("Harf yoki belgi kiritilgan bo'lishi mumkin. Iltimos qayta urunib ko'ring");
        } catch (error) {
            if (id_price.value.includes(',')) {
                $('.amount').unmask()
            }
            if (isNumber(id_kg.value) && isNumber(id_price.value)) {
                enterForm.submit();
                id_kg.value = '';
                id_price.value = '';
            } else
                alert("Harf yoki belgi kiritilgan bo'lishi mumkin. Iltimos qayta urunib ko'ring");
        }
        
    }
} catch (error) {
    // console.log(error);
}

try {
    subBtnQarz.onclick = function() {
        if (id_qarzSum.value.includes(',')) {
            $("#id_qarzSum").unmask()
        }
        if (isNumber(id_qarzSum.value)) {
            postQarz.submit();
            id_qarzSum.value = '';
        } else
            alert("Harf yoki belgi kiritilgan bo'lishi mumkin. Iltimos qayta urunib ko'ring");
    }
} catch (error) {
    
}

try {
    deleteBtn.onclick = function() {
        let res = confirm("Ma'lumotni o'chirishni xoxlaysizmi?");
        if (res){
            deleteForm.submit()
        }
    }
} catch (error) {
    
}

try {
    sendToHomeBtn.onclick = function() {
        if (id_price.value.includes(',')) id_price.value = id_price.value.replace(',','').replace(',','');
        if (id_showToAgent.value.includes(',')) id_showToAgent.value = id_showToAgent.value.replace(',','').replace(',','');
        if (isNumber(id_price.value) && isNumber(id_showToAgent.value)) {
            sendHomeForm.submit()
        } else {
            alert("Ma'lumotni kiritishda xatolik bor. Iltimos qaytadan urinib ko'ring")
        }
    }
} catch (error) {
    
}
if (fileRun) {
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
      });
}

try {
    payAgentSubBtn.onclick = () => {
        if (id_payAgent.value.includes(',')) {
            $("#id_payAgent").unmask();
        }
        
        if (isNumber(id_payAgent.value)) {
            payAgentForm.submit();
            id_payAgent.value = '';
        } 
        else
            alert("Harf yoki belgi kiritilgan bo'lishi mumkin. Iltimos qayta urunib ko'ring");
    }
} catch (error) {
    
}
try {
    lendDebtBazaBtn.onclick = function() {
        if (id_lastLendDebt.value.includes(',')) {
            $("#id_lastLendDebt").unmask();
        }
        
        if (isNumber(id_lastLendDebt.value)) {
            lendDebtBaza.submit();
            id_lastLendDebt.value = '';
        } 
        else
            alert("Harf yoki belgi kiritilgan bo'lishi mumkin. Iltimos qayta urunib ko'ring");
    }
} catch (error) {
    
}