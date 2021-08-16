const clientKey = "test_CIXAPNBW2JERLEJ6GYYC3WBLVMO2HIZ3";
const total_price = parseFloat(document.getElementById("total-price").value)*100;


async function Checkout() {
	try {		
		const paymentMethodsResponse = JSON.parse(document.getElementById("payment-options").value);
		const configuration = {
			paymentMethodsResponse: paymentMethodsResponse,
			clientKey: clientKey,
			locale: "en_US",
			environment: "test",
			showPayButton: true,
			paymentMethodsConfiguration: {
				ideal: {
					showImage: true
				},
				card: {
					hasHolderName: true,
					holderNameRequired: true,
					enableStoreDetails: true,
					showStoredPaymentMethods: true,
					name: "Credit or debit card",
					
					amount: {
						value: total_price,
						currency: "AUD"
					}
				},
				paypal: {
					amount: {
						currency: "AUD",
						value: total_price,
					},
					environment: "test", 
					countryCode: "AU", 
					intent: "authorize" 
				}
			},
			onSubmit: (state, component) => {
				console.log(state.data);

				if (state.isValid) {
								handleSubmission(state.data, component, "/api/initiatePayment/");
								}
			},
			onAdditionalDetails: (state, component) => {
				handleSubmission(state.data, component, "/api/initiatePayment/");
			}
		};

		const checkout = new AdyenCheckout(configuration);
		checkout.create('dropin',{openFirstPaymentMethod:false,showStoredPaymentMethods:true}).mount("#dropin-container");
	} catch (error) {
		console.error(error);
		alert("Something is not right, please check console for logs");
	}
}


// Event handlers called when the shopper selects the pay button,
// or when additional information is required to complete the payment
async function handleSubmission(data, component, url) {
	try {
		
		const res = await callServer(url, data);
		handleServerResponse(res, component);
	} catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	}
}

// Calls server endpoints
async function callServer(url, data) {
	const res = await fetch(url, {
		method: "POST",
		body: data ? JSON.stringify(data) : "",
		headers: {
			"Content-Type": "application/json"
		}
	});
	return await res.json();
}

// Handles responses sent from server to the client
function handleServerResponse(res, component) {
	if (res.action) {
		component.handleAction(res.action);		
	} else {
		console.log(res.resultCode)
		switch (res.resultCode) {
			case "Authorised":
				window.location.href = "/result/success";
				break;
			case "Pending":
				window.location.href = "/result/pending";
				break;
			case "Received":
				window.location.href = "/result/pending";
				break;
			case "Refused":
				window.location.href = "/result/error";
				break;
			default:
				window.location.href = "/result/error";
				break;
		}
	}
}
Checkout();
