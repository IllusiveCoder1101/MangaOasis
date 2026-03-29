<template>
    <div class="landing_page" >
        <header class="header">
            <nav class="navbar">
                <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
                <div class="button_group">
                    <router-link to="/user/register"><button class="primary">Sign-up</button></router-link>
                    <router-link to="/user/login"><button class="secondary">Sign-in</button></router-link>
                </div>
            </nav>
            <section class="hero_section">
                <div class="hero_text">
                    <h1 class="heading">Explore <em>Escape</em> Experience  </h1>
                    <p class="sub_heading">"Dive into Endless Adventures with Our Online Manga Library"</p>
                </div>
            </section>
        </header>
   
            
        <section class="features">
                <h1 class="heading1">Our Features</h1>
              
                <div class="feature_container">
                        <img src="../assets/images/feature1-img.webp" alt="features" class="feature_img">
                        <div class="feature_text_container">
                            <p class="sub_heading2">Extensive Manga Collection</p>
                            <p class="sub_desc1">Immerse yourself in a vast and diverse library with Manga Oasis, featuring an extensive collection of manga titles spanning various genres. From action-packed adventures to heartwarming romances, our carefully curated selection ensures there's something for every manga enthusiast.</p>
                        </div>
                </div>
                <div class="feature_container1">
                        <img src="../assets/images/feature2-img.webp" alt="features" class="feature_img">
                        <div class="feature_text_container">
                            <p class="sub_heading2">User-Friendly Interface</p>
                            <p class="sub_desc1">Navigate effortlessly through the enchanting worlds of manga with our intuitive and user-friendly platform. Manga Oasis is designed to provide a seamless and enjoyable experience, making it easy for both seasoned manga enthusiasts and newcomers to explore, discover, and indulge in their favorite stories.</p>
                        </div>
                </div>
                <div class="feature_container">
                        <img src="../assets/images/feature3-img.webp" alt="features" class="feature_img">
                        <div class="feature_text_container">
                            <p class="sub_heading2">English Translated Mangas</p> 
                            <p class="sub_desc1">Dive into the world of manga seamlessly with Manga Oasis, where a significant portion of our collection is thoughtfully translated into English. Enjoy an immersive reading experience without language barriers, connecting with the stories and characters in a language you understand. Manga Oasis is your gateway to a global manga community with English-translated titles, fostering an inclusive and enjoyable reading environment.</p>
                        </div>
                </div>
           
        </section>
      
        <footer class="footer">
            <p class="footer_text">© 2024 Manga Oasis. All rights reserved.</p>
            <div class="icon_group">
                <vue-feather type="youtube" class="icon" ></vue-feather>
                <vue-feather type="facebook" class="icon"></vue-feather>
                <vue-feather type="twitter" class="icon"></vue-feather>
                <vue-feather type="twitch" class="icon"></vue-feather>
             
            </div>
        </footer>
    </div>

</template>

<script setup>
    import { onMounted } from 'vue';
    onMounted(()=>{
        window.scrollTo(0,0)
    })
</script>