<template>
    <section class="modal">
        <div class="modal_container1">
            
            <header class="modal_head">
                <h1 class="modal_header">Select Banner</h1>
                <button @click="close_func()" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="banner_container">
                    <div :class="(banner_data.result=='banner1.jpg')?'active_banner':'banner_contain'">
                        <img src="../assets/images/banner1.jpg" alt="banner" class="choice_banner" @click="()=>banner_data.result='banner1.jpg'">
                    </div>
                    <div :class="(banner_data.result=='banner2.jpg')?'active_banner':'banner_contain'">
                        <img src="../assets/images/banner2.jpg" alt="banner" class="choice_banner" @click="()=>banner_data.result='banner2.jpg'">
                    </div>
                    <div :class="(banner_data.result=='banner3.jpg')?'active_banner':'banner_contain'">
                        <img src="../assets/images/banner3.jpg" alt="banner" class="choice_banner" @click="()=>banner_data.result='banner3.jpg'">
                    </div>
                    <div :class="(banner_data.result=='banner4.jpg')?'active_banner':'banner_contain'">
                        <img src="../assets/images/banner4.jpg" alt="banner" class="choice_banner" @click="()=>banner_data.result='banner4.jpg'">
                    </div>
                </div>
                <div class="payment_details">
                    <button type="submit" class="primary_btn1" @click.prevent="handle_update_banner(banner_data.result)">Add Banner</button>
                </div>
            </form>
        </div>
    </section>
</template>

<script setup>
    import { ref } from 'vue';
    const banner_data=ref({"result":""})
</script>

<script>
    export default {
        props:["close_func","handle_update_banner","current_banner"],
    }
</script>