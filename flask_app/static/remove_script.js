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