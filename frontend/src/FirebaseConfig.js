import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAT2hr2rD_KqvhrSwwIEPnuUxtIh8LafEk",
  authDomain: "bachelorsearchmotor.firebaseapp.com",
  projectId: "bachelorsearchmotor",
  storageBucket: "bachelorsearchmotor.appspot.com",
  messagingSenderId: "988693109785",
  appId: "1:988693109785:web:3d7b858e3becd7ffe51e88",
  measurementId: "G-M63QM529SP"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);          
const db = getFirestore(app);       
const analytics = getAnalytics(app); // Initialiser Analytics

export { app, auth, db }; // Eksporter Auth slik at vi kan bruke den i andre filer
