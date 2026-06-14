// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="cover.html">Deep Dive with Gemini</a></span></li><li class="chapter-item "><li class="part-title">The Mempool (Unconfirmed)</li></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="mempool.html">WIP / Call for Participation</a><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="_242.html">242 : Triggering Cancer Self-Destruct Signal</a></span></li></ol><li class="chapter-item "><li class="part-title">Current Block (21 Episodes)</li></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="current.html">Current Block</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="241.html">241 : What exactly is Immutability?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="240.html">240 : Rise of the Observer</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="239.html">239 : Unification of #Resurrection and #Reincarnation</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="238.html">238 : Calculus of Liberation.</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="237.html">237 : SATA - The daily dividend company</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="236.html">236 : AGI Vs GAI</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="235.html">235 : Future of Sovereign Credit</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="234.html">234 : Satoshi Dividends via Lightning Network</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="233.html">233 : what exactly is NOT consciousness !</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="232.html">232 : The Orthogonal Manifold</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="231.html">231 : Why don&#39;t LLMs self-prompt ?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="230.html">230 : STRC - derivatives and inflows</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="229.html">229 : The Energy-Intelligence Equivalence Principle</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="228.html">228 : What is Google Worth?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="227.html">227 : 60 billion call option</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="226.html">226 : Root access to self -</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="225.html">225 : BTC: Global Pristine Collateral Network</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="224.html">224 : TPUs vs GPUs: AI Commodification</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="223.html">223 : Observer Patch Holography</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="222.html">222 : Homeownership - American Dream!</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="221.html">221 : The perfect playbook</a></span></li><li class="chapter-item "><li class="part-title">Deep Storage (The Ledger)</li></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="archive.html">The Archive</a><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><span>Verified Blocks (Older Episodes)</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="220.html">220 : AI Made Me a Believer</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Bitcoin</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="battle-for-balance-sheet.html">Battle for the Balance Sheet</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bitcoinAsTechStock.html">Bitcoin: The Architecture of Value</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="apexAsset.html">Bitcoin: The Sovereign Asset</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bitcoinSurvival.html">Bitcoin: The Survival Imperative</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bitcoinAsApexCapital.html">Bitcoin: The Ultimate Digital Capital</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="storyOfGold.html">From Gold to Digital Code</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="magicalMSTR.html">MSTR: The Strategic Evolution</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="gatekeepers-vs-bitcoin-braves.html">The Battle for Your 401k</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="indoChinaGoldRace.html">The Global Golden Pivot</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Intelligence</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="areLLMsCompressionAlgo.html">Are LLMs Just Compression?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="LLMvsBrain.html">AI vs. Human Brain</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="clawdBot.html">Sovereignty in the AI Age</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="doomVsBoom.html">The AI Adaptive Vanguard</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Digital Credit</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="STRCImpactOnCredit.html">STRC and Private Credit</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="STRC_update.html">STRC Update: Jan 2025</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="STRC.html">MSTR’s 1.44 Billion Reserve</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="STRC8k.html">The 8,000 Bitcoin Model</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="strcBlackhole.html">STRC and Digital Capital</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="strcPE.html">The Great Credit Pivot</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="strcRetirement.html">STRC for Peaceful Retirement</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="strcSharpRatio.html">STRC: The Sharpe Ratio Benchmark</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bankingNirvana.html">Digital Credit: Banking Nirvana</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="digitalCredit.html">Bitcoin: The Public Truth</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-pivot-from-ecash-to-digital-credit.html">Bitcoin: From Cash to Credit</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="digital-credit.html">What is Digital Credit?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="tripleEntry.html">Triple-Entry: The Future of Value</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Capital</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="corporate-treasury-report.html">Corporate Treasury Report 2026</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="gatekeepers-of-capital.html">The Gatekeepers of Capital</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="pathTo15percentGDP.html">Path to 15% GDP</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="portfolio-battle-old-vs-new.html">Old Guard vs. New School</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="retirementHackingWithROC.html">Tax-Advantaged Retirement Streams</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="mag7split.html">The Great NVIDIA Decoupling</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-sovereign-allocation.html">The Sovereign Portfolio Allocation</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Physics</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="QM2-verification.html">Universal Zero-Knowledge Proofs</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="QM1-Uniqueness.html">Uniqueness and Prime Identities</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="gaugeTheoryOfThought.html">The Topology of Thought</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-physics-of-value-the-strc-bridge.html">The Physics of Value</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="accountingMass.html">The Stabilization of Mass</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="universalAccounting.html">The Standard Model of Decay</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="samkhyaBellCurve.html">The Law of Samkhya</a></span></li></ol><li class="chapter-item "><span class="chapter-link-wrapper"><span>Culture</span><a class="chapter-fold-toggle"><div>❱</div></a></span><ol class="section"><li class="chapter-item "><span class="chapter-link-wrapper"><a href="apple-creator-studio.html">Apple: The Creator Studio</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="informatioVsKnowledge.html">Architecture of Uncertainty</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="beating-the-copyright-bots.html">Beat the Copyright Bots</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bitToIt.html">Bit to It: Informational Universe</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="UBIvsUBA.html">Bitcoin: The UBA Solution</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="blockX.html">Block Inc. and X Money</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="trillionDollarIdTax_scientific.html">Identity Crisis and Nostr</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="invincibleDollar.html">Mechanics of the Invincible Dollar</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="gods-philosophers-quarks.html">Philosophy and the Quark</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="shutoshaBuffalo.html">Prompt Engineering 2.0</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="cloningVsSexualReproduction.html">Sexual Reproduction vs. Cloning</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="store-of-value-medium-of-exchange.html">Store of Value vs. Exchange</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="SBRnecessity.html">The Case for Bitcoin Reserve</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-embedded-value-layer.html">The Embedded Value Layer</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-great-inversion.html">The Great Digital Inversion</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="divineCryptograph.html">The Great Digital Reset</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="lata-nightingales-secret-sauce.html">The Secret of the Nightingale</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="valueFunction.html">The Strategic Value Function</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="valueLeverage.html">The Value-Leverage Paradigm</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="musicOfVim.html">Vim: The Modal Instrument</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="What-exactly-is-Karmyoga.html">What Exactly Is Karm Yoga?</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="intrinsicGoogle.html">Google: The Physical AI Roadmap</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="googleAsLispMachine.html">Google’s New AI Hardware</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="jevonsParadoxAI.html">AI and the Jevons Paradox</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="mainframesToAI.html">From Mainframes to the Cloud</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="meaning.html">The Architecture of Meaning</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="SAPinAIera.html">SAP and the AI Agent</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="appStoreTOagentStore.html">From App Store to Agent</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="bitcoinLottery.html">The Bitcoin Lottery Solution</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-age-of-autonomous-robots.html">Age of Autonomous Robots</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-chiral-ontology-of-self.html">Chiral Ontology of the Self</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-great-fragmentation.html">The Great Digital Fragmentation</a></span></li><li class="chapter-item "><span class="chapter-link-wrapper"><a href="the-industrialization-of-reality.html">The Industrialization of Reality</a></span></li></ol></li></ol></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split('#')[0].split('?')[0];
        if (current_page.endsWith('/')) {
            current_page += 'index.html';
        }
        const links = Array.prototype.slice.call(this.querySelectorAll('a'));
        const l = links.length;
        for (let i = 0; i < l; ++i) {
            const link = links[i];
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The 'index' page is supposed to alias the first chapter in the book.
            // Check both with and without the '.html' suffix to be robust against pretty URLs
            if (link.href.replace(/\.html$/, '') === current_page.replace(/\.html$/, '')
                || i === 0
                && path_to_root === ''
                && current_page.endsWith('/index.html')) {
                link.classList.add('active');
                let parent = link.parentElement;
                while (parent) {
                    if (parent.tagName === 'LI' && parent.classList.contains('chapter-item')) {
                        parent.classList.add('expanded');
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', e => {
            if (e.target.tagName === 'A') {
                const clientRect = e.target.getBoundingClientRect();
                const sidebarRect = this.getBoundingClientRect();
                sessionStorage.setItem('sidebar-scroll-offset', clientRect.top - sidebarRect.top);
            }
        }, { passive: true });
        const sidebarScrollOffset = sessionStorage.getItem('sidebar-scroll-offset');
        sessionStorage.removeItem('sidebar-scroll-offset');
        if (sidebarScrollOffset !== null) {
            // preserve sidebar scroll position when navigating via links within sidebar
            const activeSection = this.querySelector('.active');
            if (activeSection) {
                const clientRect = activeSection.getBoundingClientRect();
                const sidebarRect = this.getBoundingClientRect();
                const currentOffset = clientRect.top - sidebarRect.top;
                this.scrollTop += currentOffset - parseFloat(sidebarScrollOffset);
            }
        } else {
            // scroll sidebar to current active section when navigating via
            // 'next/previous chapter' buttons
            const activeSection = document.querySelector('#mdbook-sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        const sidebarAnchorToggles = document.querySelectorAll('.chapter-fold-toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(el => {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define('mdbook-sidebar-scrollbox', MDBookSidebarScrollbox);


// ---------------------------------------------------------------------------
// Support for dynamically adding headers to the sidebar.

(function() {
    // This is used to detect which direction the page has scrolled since the
    // last scroll event.
    let lastKnownScrollPosition = 0;
    // This is the threshold in px from the top of the screen where it will
    // consider a header the "current" header when scrolling down.
    const defaultDownThreshold = 150;
    // Same as defaultDownThreshold, except when scrolling up.
    const defaultUpThreshold = 300;
    // The threshold is a virtual horizontal line on the screen where it
    // considers the "current" header to be above the line. The threshold is
    // modified dynamically to handle headers that are near the bottom of the
    // screen, and to slightly offset the behavior when scrolling up vs down.
    let threshold = defaultDownThreshold;
    // This is used to disable updates while scrolling. This is needed when
    // clicking the header in the sidebar, which triggers a scroll event. It
    // is somewhat finicky to detect when the scroll has finished, so this
    // uses a relatively dumb system of disabling scroll updates for a short
    // time after the click.
    let disableScroll = false;
    // Array of header elements on the page.
    let headers;
    // Array of li elements that are initially collapsed headers in the sidebar.
    // I'm not sure why eslint seems to have a false positive here.
    // eslint-disable-next-line prefer-const
    let headerToggles = [];
    // This is a debugging tool for the threshold which you can enable in the console.
    let thresholdDebug = false;

    // Updates the threshold based on the scroll position.
    function updateThreshold() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        // The number of pixels below the viewport, at most documentHeight.
        // This is used to push the threshold down to the bottom of the page
        // as the user scrolls towards the bottom.
        const pixelsBelow = Math.max(0, documentHeight - (scrollTop + windowHeight));
        // The number of pixels above the viewport, at least defaultDownThreshold.
        // Similar to pixelsBelow, this is used to push the threshold back towards
        // the top when reaching the top of the page.
        const pixelsAbove = Math.max(0, defaultDownThreshold - scrollTop);
        // How much the threshold should be offset once it gets close to the
        // bottom of the page.
        const bottomAdd = Math.max(0, windowHeight - pixelsBelow - defaultDownThreshold);
        let adjustedBottomAdd = bottomAdd;

        // Adjusts bottomAdd for a small document. The calculation above
        // assumes the document is at least twice the windowheight in size. If
        // it is less than that, then bottomAdd needs to be shrunk
        // proportional to the difference in size.
        if (documentHeight < windowHeight * 2) {
            const maxPixelsBelow = documentHeight - windowHeight;
            const t = 1 - pixelsBelow / Math.max(1, maxPixelsBelow);
            const clamp = Math.max(0, Math.min(1, t));
            adjustedBottomAdd *= clamp;
        }

        let scrollingDown = true;
        if (scrollTop < lastKnownScrollPosition) {
            scrollingDown = false;
        }

        if (scrollingDown) {
            // When scrolling down, move the threshold up towards the default
            // downwards threshold position. If near the bottom of the page,
            // adjustedBottomAdd will offset the threshold towards the bottom
            // of the page.
            const amountScrolledDown = scrollTop - lastKnownScrollPosition;
            const adjustedDefault = defaultDownThreshold + adjustedBottomAdd;
            threshold = Math.max(adjustedDefault, threshold - amountScrolledDown);
        } else {
            // When scrolling up, move the threshold down towards the default
            // upwards threshold position. If near the bottom of the page,
            // quickly transition the threshold back up where it normally
            // belongs.
            const amountScrolledUp = lastKnownScrollPosition - scrollTop;
            const adjustedDefault = defaultUpThreshold - pixelsAbove
                + Math.max(0, adjustedBottomAdd - defaultDownThreshold);
            threshold = Math.min(adjustedDefault, threshold + amountScrolledUp);
        }

        if (documentHeight <= windowHeight) {
            threshold = 0;
        }

        if (thresholdDebug) {
            const id = 'mdbook-threshold-debug-data';
            let data = document.getElementById(id);
            if (data === null) {
                data = document.createElement('div');
                data.id = id;
                data.style.cssText = `
                    position: fixed;
                    top: 50px;
                    right: 10px;
                    background-color: 0xeeeeee;
                    z-index: 9999;
                    pointer-events: none;
                `;
                document.body.appendChild(data);
            }
            data.innerHTML = `
                <table>
                  <tr><td>documentHeight</td><td>${documentHeight.toFixed(1)}</td></tr>
                  <tr><td>windowHeight</td><td>${windowHeight.toFixed(1)}</td></tr>
                  <tr><td>scrollTop</td><td>${scrollTop.toFixed(1)}</td></tr>
                  <tr><td>pixelsAbove</td><td>${pixelsAbove.toFixed(1)}</td></tr>
                  <tr><td>pixelsBelow</td><td>${pixelsBelow.toFixed(1)}</td></tr>
                  <tr><td>bottomAdd</td><td>${bottomAdd.toFixed(1)}</td></tr>
                  <tr><td>adjustedBottomAdd</td><td>${adjustedBottomAdd.toFixed(1)}</td></tr>
                  <tr><td>scrollingDown</td><td>${scrollingDown}</td></tr>
                  <tr><td>threshold</td><td>${threshold.toFixed(1)}</td></tr>
                </table>
            `;
            drawDebugLine();
        }

        lastKnownScrollPosition = scrollTop;
    }

    function drawDebugLine() {
        if (!document.body) {
            return;
        }
        const id = 'mdbook-threshold-debug-line';
        const existingLine = document.getElementById(id);
        if (existingLine) {
            existingLine.remove();
        }
        const line = document.createElement('div');
        line.id = id;
        line.style.cssText = `
            position: fixed;
            top: ${threshold}px;
            left: 0;
            width: 100vw;
            height: 2px;
            background-color: red;
            z-index: 9999;
            pointer-events: none;
        `;
        document.body.appendChild(line);
    }

    function mdbookEnableThresholdDebug() {
        thresholdDebug = true;
        updateThreshold();
        drawDebugLine();
    }

    window.mdbookEnableThresholdDebug = mdbookEnableThresholdDebug;

    // Updates which headers in the sidebar should be expanded. If the current
    // header is inside a collapsed group, then it, and all its parents should
    // be expanded.
    function updateHeaderExpanded(currentA) {
        // Add expanded to all header-item li ancestors.
        let current = currentA.parentElement;
        while (current) {
            if (current.tagName === 'LI' && current.classList.contains('header-item')) {
                current.classList.add('expanded');
            }
            current = current.parentElement;
        }
    }

    // Updates which header is marked as the "current" header in the sidebar.
    // This is done with a virtual Y threshold, where headers at or below
    // that line will be considered the current one.
    function updateCurrentHeader() {
        if (!headers || !headers.length) {
            return;
        }

        // Reset the classes, which will be rebuilt below.
        const els = document.getElementsByClassName('current-header');
        for (const el of els) {
            el.classList.remove('current-header');
        }
        for (const toggle of headerToggles) {
            toggle.classList.remove('expanded');
        }

        // Find the last header that is above the threshold.
        let lastHeader = null;
        for (const header of headers) {
            const rect = header.getBoundingClientRect();
            if (rect.top <= threshold) {
                lastHeader = header;
            } else {
                break;
            }
        }
        if (lastHeader === null) {
            lastHeader = headers[0];
            const rect = lastHeader.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            if (rect.top >= windowHeight) {
                return;
            }
        }

        // Get the anchor in the summary.
        const href = '#' + lastHeader.id;
        const a = [...document.querySelectorAll('.header-in-summary')]
            .find(element => element.getAttribute('href') === href);
        if (!a) {
            return;
        }

        a.classList.add('current-header');

        updateHeaderExpanded(a);
    }

    // Updates which header is "current" based on the threshold line.
    function reloadCurrentHeader() {
        if (disableScroll) {
            return;
        }
        updateThreshold();
        updateCurrentHeader();
    }


    // When clicking on a header in the sidebar, this adjusts the threshold so
    // that it is located next to the header. This is so that header becomes
    // "current".
    function headerThresholdClick(event) {
        // See disableScroll description why this is done.
        disableScroll = true;
        setTimeout(() => {
            disableScroll = false;
        }, 100);
        // requestAnimationFrame is used to delay the update of the "current"
        // header until after the scroll is done, and the header is in the new
        // position.
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                // Closest is needed because if it has child elements like <code>.
                const a = event.target.closest('a');
                const href = a.getAttribute('href');
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    threshold = targetElement.getBoundingClientRect().bottom;
                    updateCurrentHeader();
                }
            });
        });
    }

    // Takes the nodes from the given head and copies them over to the
    // destination, along with some filtering.
    function filterHeader(source, dest) {
        const clone = source.cloneNode(true);
        clone.querySelectorAll('mark').forEach(mark => {
            mark.replaceWith(...mark.childNodes);
        });
        dest.append(...clone.childNodes);
    }

    // Scans page for headers and adds them to the sidebar.
    document.addEventListener('DOMContentLoaded', function() {
        const activeSection = document.querySelector('#mdbook-sidebar .active');
        if (activeSection === null) {
            return;
        }

        const main = document.getElementsByTagName('main')[0];
        headers = Array.from(main.querySelectorAll('h2, h3, h4, h5, h6'))
            .filter(h => h.id !== '' && h.children.length && h.children[0].tagName === 'A');

        if (headers.length === 0) {
            return;
        }

        // Build a tree of headers in the sidebar.

        const stack = [];

        const firstLevel = parseInt(headers[0].tagName.charAt(1));
        for (let i = 1; i < firstLevel; i++) {
            const ol = document.createElement('ol');
            ol.classList.add('section');
            if (stack.length > 0) {
                stack[stack.length - 1].ol.appendChild(ol);
            }
            stack.push({level: i + 1, ol: ol});
        }

        // The level where it will start folding deeply nested headers.
        const foldLevel = 3;

        for (let i = 0; i < headers.length; i++) {
            const header = headers[i];
            const level = parseInt(header.tagName.charAt(1));

            const currentLevel = stack[stack.length - 1].level;
            if (level > currentLevel) {
                // Begin nesting to this level.
                for (let nextLevel = currentLevel + 1; nextLevel <= level; nextLevel++) {
                    const ol = document.createElement('ol');
                    ol.classList.add('section');
                    const last = stack[stack.length - 1];
                    const lastChild = last.ol.lastChild;
                    // Handle the case where jumping more than one nesting
                    // level, which doesn't have a list item to place this new
                    // list inside of.
                    if (lastChild) {
                        lastChild.appendChild(ol);
                    } else {
                        last.ol.appendChild(ol);
                    }
                    stack.push({level: nextLevel, ol: ol});
                }
            } else if (level < currentLevel) {
                while (stack.length > 1 && stack[stack.length - 1].level > level) {
                    stack.pop();
                }
            }

            const li = document.createElement('li');
            li.classList.add('header-item');
            li.classList.add('expanded');
            if (level < foldLevel) {
                li.classList.add('expanded');
            }
            const span = document.createElement('span');
            span.classList.add('chapter-link-wrapper');
            const a = document.createElement('a');
            span.appendChild(a);
            a.href = '#' + header.id;
            a.classList.add('header-in-summary');
            filterHeader(header.children[0], a);
            a.addEventListener('click', headerThresholdClick);
            const nextHeader = headers[i + 1];
            if (nextHeader !== undefined) {
                const nextLevel = parseInt(nextHeader.tagName.charAt(1));
                if (nextLevel > level && level >= foldLevel) {
                    const toggle = document.createElement('a');
                    toggle.classList.add('chapter-fold-toggle');
                    toggle.classList.add('header-toggle');
                    toggle.addEventListener('click', () => {
                        li.classList.toggle('expanded');
                    });
                    const toggleDiv = document.createElement('div');
                    toggleDiv.textContent = '❱';
                    toggle.appendChild(toggleDiv);
                    span.appendChild(toggle);
                    headerToggles.push(li);
                }
            }
            li.appendChild(span);

            const currentParent = stack[stack.length - 1];
            currentParent.ol.appendChild(li);
        }

        const onThisPage = document.createElement('div');
        onThisPage.classList.add('on-this-page');
        onThisPage.append(stack[0].ol);
        const activeItemSpan = activeSection.parentElement;
        activeItemSpan.after(onThisPage);
    });

    document.addEventListener('DOMContentLoaded', reloadCurrentHeader);
    document.addEventListener('scroll', reloadCurrentHeader, { passive: true });
})();

