<script>
    import CustomDatepicker from "./CustomDatepicker.svelte";
    import dayjs from "dayjs";

    let store;
    const query = new URLSearchParams(window.location.search)
    const urlDate = query.get('filter_date')
    let defaultDate, selectedDate
    if (urlDate) {
        const [day, month, year] = urlDate.split('-')
        defaultDate = selectedDate = new Date(+year, +month - 1, +day)

    }


    $: if (store) {
        console.log({selectedDate})
        if(defaultDate) store.getState().hasChosen = true
        store.subscribe((storeInfo) => {
            if (storeInfo.hasChosen && !storeInfo.open && !storeInfo.enlargeDay) {
                console.log({storeInfo})
                if(store.getState().selected !== defaultDate){
                    query.set("filter_date", dayjs(store.getState().selected).format("DD-MM-YYYY"))
                    const url = window.location.origin + window.location.pathname + '?' + query.toString()
                    window.location.href = url
                }
            }
        })
    }
</script>

<CustomDatepicker bind:store bind:selected="{selectedDate}" automaticHasChosenOnDefault="{false}"/>
