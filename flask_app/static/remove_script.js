function removeHandler(e, item) {
    console.log(item)
    let confirmed = confirm(`Are you sure you want to remove ${item} from the order entirely?`)
    if (!confirmed){
        e.preventDefault()
    }
}