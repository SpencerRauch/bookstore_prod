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

function shipHandler(e,with_auto_fill=false){
    let confirmed;
    if (with_auto_fill){
        confirmed = confirm(`This action will attempt to adjust all shipped quantities to ordered quantities. If this is successful, sales order will be finalized as shipped in full and inventory will be affected. If order cannot be shipped in full, errors will show on lines that do not have enough stock`)
    } else {
        confirmed = confirm(`This action will finalizing shipping with current shipped values. Inventory will be affected.`)
    }
    if (!confirmed){
        e.preventDefault()
    }        
}