<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Edit Review</h1>
                <button @click="close_func(data['feedback_id'])" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="review_details">
                    <div class="detail_container4">
                        <label for="score" class="modal_label">Score</label>
                        <input type="number" @input="feedback_data['feedback_score']=$event.target.value" :value="data['feedback_score']"  id="score" placeholder="0" class="modal_input3" required>
                    </div>
                    <div class="detail_container4">
                        <label for="comment" class="modal_label">Comment</label>
                        <textarea  id="comment" @input="feedback_data['feedback_message']=$event.target.value" :value="data['feedback_message']" cols="60" rows="7" class="modal_input2" placeholder="Write Your Views" required></textarea>
                    </div>
                </div>
                <button type="submit" class="primary_btn1" @click.prevent="()=>handle_submit(data['feedback_id'],feedback_data)">Submit Review</button>
                
            </form>
        </div>
    </section>
</template>
<script setup>
    import { ref } from 'vue';
    const feedback_data=ref({"feedback_message":"","feedback_score":0}) 
</script>
<script>
    export default {
        props:["close_func","handle_submit","data"]
    }
</script>