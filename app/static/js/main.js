let header = document.getElementsByTagName('h3')[0]


//function likeHandler(){
//    console.log("likeHandler");
//};


//   window.fbAsyncInit = function() {
//     FB.init({
//       appId      : '{your-app-id}',
//       cookie     : true,
//       xfbml      : true,
//       version    : '{api-version}'
//     });

//     FB.AppEvents.logPageView();   

//   };

//   (function(d, s, id){
//      var js, fjs = d.getElementsByTagName(s)[0];
//      if (d.getElementById(id)) {return;}
//      js = d.createElement(s); js.id = id;
//      js.src = "https://connect.facebook.net/en_US/sdk.js";
//      fjs.parentNode.insertBefore(js, fjs);
//    }(document, 'script', 'facebook-jssdk'));

// response

// {
//     status: 'connected',
//     authResponse: {
//         accessToken: '...',
//         expiresIn:'...',
//         signedRequest:'...',
//         userID:'...'
//     }
// }

// status specifies the login status of the person using the app. The status can be one of the following:
// connected - the person is logged into Facebook, and has logged into your app.
// not_authorized - the person is logged into Facebook, but has not logged into your app.
// unknown - the person is not logged into Facebook, so you don't know if they've logged into your app or FB.logout() was called before and therefore, it cannot connect to Facebook.
// authResponse is included if the status is connected and is made up of the following:
// accessToken - contains an access token for the person using the app.
// expiresIn - indicates the UNIX time when the token expires and needs to be renewed.
// signedRequest - a signed parameter that contains information about the person using the app.
// userID - the ID of the person using the app.
// Once your app knows the login status of the person using it, it can do one of the following:
// If the person is logged into Facebook and your app, redirect them to your app's logged in experience.
// If the person isn't logged into your app, or isn't logged into Facebook, prompt them with the Login dialog with FB.login() or show them the Login Button.

// Including the Login Button into your page is easy. Visit the documentation for the login button and set the button up the way you want. Then click Get Code and it will show you the code you need to display the button on your page.
// The onlogin attribute on the button to set up a JavaScript callback that checks the login status to see if the person logged in successfully:

{/* <fb:login-button 
  scope="public_profile,email"
  onlogin="checkLoginState();">
</fb:login-button> */}

// This is the callback. It calls FB.getLoginStatus() to get the most recent login state. (statusChangeCallback() is a function that's part of the example that processes the response.)

// function checkLoginState() {
//     FB.getLoginStatus(function(response) {
//       statusChangeCallback(response);
//     });
//   }