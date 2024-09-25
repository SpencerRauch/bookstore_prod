function removeHandler(e, item) {
    console.log(item)
    let confirmed = confirm(`Are you sure you want to remove ${item} from the order entirely?`)
    if (!confirmed){
        e.preventDefault()
    }
}

function finalizeHandler(e){
    let confirmed = confirm(`Are you sure you want to mark this order as ready to pick?`)
    if (!confirmed){
        e.preventDefault()
    }    
}

function cancelHandler(e){
    let confirmed = confirm(`Are you sure you want to cancel this order?`)
    if (!confirmed){
        e.preventDefault()
    }        
}

function finalizeHandlerPO(e){
    let confirmed = confirm(`Are you sure you want to mark this purchase order as ready to receive?`)
    if (!confirmed){
        e.preventDefault()
    }    
}

function cancelHandlerPO(e){
    let confirmed = confirm(`Are you sure you want to cancel this purchase order?`)
    if (!confirmed){
        e.preventDefault()
    }        
}

function shipHandler(e,with_auto_fill=false){
    let confirmed;
    if (with_auto_fill){
        confirmed = confirm(`This action will attempt to adjust all shipped quantities to ordered quantities barring any shortages. This will overwrite existing shipped quantities`)
    } else {
        confirmed = confirm(`This action will finalizing shipping with current shipped values. Inventory will be affected.`)
    }
    if (!confirmed){
        e.preventDefault()
    }        
}
function receiveHandler(e,with_auto_fill=false){
    let confirmed;
    if (with_auto_fill){
        confirmed = confirm(`This action will adjust all received quantities to ordered quantities. This will overwrite existing received quantities`)
    } else {
        confirmed = confirm(`This action will finalize the receipt of the purchase order. Inventory will be affected.`)
    }
    if (!confirmed){
        e.preventDefault()
    }        
}