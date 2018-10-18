document.addEventListener("DOMContentLoaded",() => {
    const queryParams = getQueryParams();

    let pageController = new PageController(enterpriseMode=!!queryParams.enterpriseMode);
    pageController.showIntroIfNew();
    pageController.beginAnimations();
})

const getQueryParams = () => {
    try{
        url = window.location.href;
        query_str = url.substr(url.indexOf('?')+1, url.length-1);
        r_params = query_str.split('&');
        params = {}
        for( i in r_params){
            param = r_params[i].split('=');
            params[ param[0] ] = param[1] || true;
        }
        return params;
    }
    catch(e){
       return {};
    }
}

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const rand = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}

let animationStates = {
    idle: 0,
    squinting: 2,
    talking: 3,
    sleeping: 4
}

let blinkAnimation = {
    run: (context) => {
        var lastBlink = 0;
        let blinkInterval = 5500;

        setInterval(() => {
            if((new Date()).getTime() - lastBlink > blinkInterval) {
                lastBlink = (new Date()).getTime();

                (async () => {
                    context.svg.classList.add('blinking')
                    await sleep(200)
                    context.svg.classList.remove('blinking')
                    await sleep(400)
                    context.svg.classList.add('blinking')
                    await sleep(200)
                    context.svg.classList.remove('blinking')
                })();
            }
        }, 100)
    }
}

let wakeUpAnimation = {
    run: (context) => {
        (async() => {
            context.svg.classList.add('wake-up')
            await sleep(2000)
            context.svg.classList.remove('wake-up')
        })()
    }
}

let idleState = {
    enter: (context) => {
        context.svg.classList.add('idling')

        context.state = { }
    },
    tick: (context) => { },
    leave: (context) => {
        context.state = null;
        context.svg.classList.remove('idling')
        context.svg.classList.remove('blinking')
    }
}

let squintState = {
    enter: (context) => {
        context.svg.classList.add('squinting')
    },
    tick: (context) => { },
    leave: (context) => {
        context.svg.classList.remove('squinting')
    }
}

let sleepingState = {
    enter: (context) => {
        context.svg.classList.add('sleeping')
    },
    tick: (context) => { },
    leave: (context) => {
        context.svg.classList.remove('sleeping')
    }
}

let talkState = {
    enter: (context) => {
        context.svg.classList.add('talking')

        context.state = {
            lastTalk: 0,
            talkInterval: [100, 350]
        }
    },
    tick: (context) => {
        const randTalkInterval = rand(context.state.talkInterval[0], context.state.talkInterval[1]);

        if((new Date()).getTime() - context.state.lastTalk > randTalkInterval) {
            context.state.lastTalk = (new Date()).getTime();

            (async () => {
                context.svg.classList.add('mouth-open')
                await sleep(rand(randTalkInterval*.5, randTalkInterval*.8));
                context.svg.classList.remove('mouth-open')
            })();
        }
    },
    leave: (context) => {
        context.svg.classList.remove('talking')
    }
}

const YodaController = function(svg) {
    this.svg = svg;
    this.animationContext = {
        svg: svg,
        start: (new Date()).getTime(),
        lastTransition: 0
    }
    this.animationMap = {};
    this.animationMap[animationStates.idle] = idleState;
    this.animationMap[animationStates.squinting] = squintState;
    this.animationMap[animationStates.talking] = talkState;
    this.animationMap[animationStates.sleeping] = sleepingState;

    this.animationInterval = null;
    this.transitionTo(animationStates.sleeping);
}

YodaController.prototype = {
    beginAnimationLoop: function() {
        clearInterval(this.animationInterval);
        blinkAnimation.run(this.animationContext);
        this.animationInterval = setInterval(this._animationLoop.bind(this), 100);
    },
    transitionTo: function(animationState, delay) {
        const requestedTransition = this.animationMap[animationState];
        if(requestedTransition == this.animationState) return;

        if(this.animationState)
            this.animationState.leave(this.animationContext);

        this.animationContext.lastTransition = (new Date()).getTime();
        this.animationState = requestedTransition;

        if(delay)
            setTimeout(() => this.animationState.enter(this.animationContext), delay || 0);
        else
            this.animationState.enter(this.animationContext)
    },
    wakeUp: function() {
        if(this.animationState == sleepingState) {
            wakeUpAnimation.run(this.animationContext);
            setTimeout(() => this.animationState == sleepingState && this.transitionTo(animationStates.idle), 1900)
        }
    },
    _animationLoop: function() {
        this.animationState.tick(this.animationContext);
    }
}

const PageController = function(enterpriseMode) {
    this.enterpriseMode = enterpriseMode;
    if(this.enterpriseMode)
        document.querySelector('body').classList.add('enterprise')

    let svg = document.querySelector('svg');
    this.yodaController = new YodaController(svg);

    this.loginWrap = document.querySelector('.log-in')
    this.loginButton = document.querySelector('.log-in .button');
    this.loginButton.addEventListener('click', this.login.bind(this));
    this.tokenInput = document.querySelector('.log-in input')

    this.wakeUpWrap = document.querySelector('.wake-up');
    this.introButton = document.querySelector('.wake-up .button');
    this.introButton.addEventListener('click', this.wakeUp.bind(this))

    this.inputsWrap = document.querySelector('.inputs');
    this.phraseInput = document.querySelector('.inputs .controls input');
    this.phraseInput.addEventListener('input', this.phraseChange.bind(this));

    this.goButton = document.querySelector('.inputs .controls .button');
    this.goButton.addEventListener('click', this.translatePhrase.bind(this))

    this.resultContainer = document.querySelector('.inputs .result');

    if(this.enterpriseMode) {
        this.wakeUpWrap.style.display = 'none';
        this.loginWrap.style.display = 'block';

        this.tokenInput.value = this.getToken()
    }
}

PageController.prototype = {
    getToken: function() {
        return window.localStorage.getItem('loginToken');
    },
    login: function() {
        const token = this.tokenInput.value.trim();
        if(token.length) {
            window.localStorage.setItem('loginToken', token);
            this.loginWrap.classList.add('fade-out-fast');
            this.wakeUpWrap.classList.add('fade-in-fast');
        }
    },
    showIntroIfNew: function() {
        if(!window.localStorage.getItem('introShown')) {
            document.querySelector('#intro').style.display = 'block';
            window.localStorage.setItem('introShown', true);
            setTimeout(() => document.querySelector('#intro').classList.add('fade-out'), 26 * 1000)
        }
    },
    beginAnimations: function() {
        this.yodaController.beginAnimationLoop();
    },
    wakeUp: function() {
        this.yodaController.wakeUp();
        this.wakeUpWrap.classList.remove('fade-in-fast');
        this.wakeUpWrap.classList.add('fade-out-fast');
        this.inputsWrap.classList.add('fade-in-fast');
    },
    phraseChange: function() {
        if(this.getPhrase().length > 0) {
            this.yodaController.transitionTo(animationStates.squinting)
            this.goButton.style.opacity = 1;
        }else{
            this.yodaController.transitionTo(animationStates.idle)
            this.goButton.style.opacity = 0;
        }
    },
    getPhrase: function() {
        return this.phraseInput.value.trim();
    },
    setInputInteractive: function(interactive) {
        this.goButton.disabled = !interactive;
        this.phraseInput.disabled = !interactive;
    },
    setResult: function(result, isError) {
        this.resultContainer.classList.add('fade-in-fast');
        this.resultContainer.innerHTML = result;
        if(isError) {
            this.resultContainer.classList.add('error')
        }else{
            this.resultContainer.classList.remove('error')
        }
    },
    translatePhrase: async function() {
        this.resultContainer.classList.remove('fade-in-fast');
        this.resultContainer.classList.add('fade-out-fast');
        let lastTalk = (new Date()).getTime();
        this.lastTalk = lastTalk;

        try {
            const phrase = this.getPhrase();
            this.setInputInteractive(false);
            let headers = {
                'Content-Type': 'application/json',
            }
            !!this.getToken() && (headers.Authorization = 'Token ' + this.getToken())

            let rawResponse = await fetch('http://localhost:8080/api/translations/', {
                method: 'POST',
                headers: headers,
                redirect: 'follow',
                body: JSON.stringify({ request: phrase })
            });
            if(rawResponse.status >= 200 && rawResponse.status < 300) {
                let data = await rawResponse.json();
                this.setResult(data.response);
            }else{
                this.setResult("Server error, there was.  Status code " + rawResponse.status, isError=true)
            }
        }catch{
            this.setResult("Translate that phrase, Yoda could not.", isError=true);
        }finally{
            this.setInputInteractive(true);
            // always talk the phrase
            this.yodaController.transitionTo(animationStates.talking);
            await sleep(5000);
            this.lastTalk == lastTalk && this.yodaController.animationState == talkState && this.yodaController.transitionTo(animationStates.idle);
        }
    }
}