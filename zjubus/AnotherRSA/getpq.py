import gmpy2
r = 110558900427544161346504752362718976801534804435890493644257478873506232592785614992145379826683391671126840529018221373402452098828015694493078067601072995198608571756276705866780317421124835052913956859542136919148942714490680148481957345248566879698301472957874467350995829768861505431281723325484600249836

n = 0x009d70ebf2737cb43a7e0ef17b6ce467ab9a116efedbecf1ead94c83e5a082811009100708d690c43c3297b787426b926568a109894f1c48257fc826321177058418e595d16aed5b358d61069150cea832cc7f2df884548f92801606dd3357c39a7ddc868ca8fa7d64d6b64a7395a3247c069112698a365a77761db6b97a2a03a5

m = n-r+1

sqrt, _ = gmpy2.isqrt_rem(m**2-4*n)

p = (m-sqrt)/2
q = (m+sqrt)/2

# Why the hell am i doing this? pq is useless