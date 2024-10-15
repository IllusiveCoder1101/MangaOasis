<template>
    <div class="carousel_container">

        <img :src="get_manga_img(book_value['book_cover'])" alt="manga_pics" class="carousel_img">
        <div class="sub_section">
            <img :src="get_manga_img(book_value['book_cover'])" alt="manga_icon" class="carousel_icon">
            <div class="carousel_text">
                <h1 class="heading">{{ book_value["book_name"]  }}</h1>
                <p class="sub_heading2">{{ book_value["author_name"] }}</p>
        
                <p class="desc">{{ book_value["book_description"].substring(0,300) }},... <span><button class="info_btn" @click="()=>handle_redirect(book_value['book_id'],user_id)">More Info</button></span></p>
                <div class="genre_list">
                    <p class="genre_name" v-for="i in book_value['book_genres'].split(',')" :key="i">{{ i }}</p>
                </div>
            </div>
        </div>

    </div> 
</template>

<script>
    export default {
        'props':["book_value","handle_redirect","user_id"],
        methods:{
            get_manga_img(pic){
                return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
            }
        }
    }
</script>
