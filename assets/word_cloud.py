import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Stopwords to exclude common words from the word cloud
stopwords = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
    "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", 
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", 
    "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "via", "was", "we", "we'd", "we'll", "we're",
    "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
])

# 1. Get the paper list from the user
# papers_input = input("Please provide the list of papers:\n")
papers_input = """
- [Adaptive Locomotion Learning for Quadruped Robots by Combining DRL with a Cosine Oscillator Based Rhythm Controller](https://www.mdpi.com/2076-3417/13/19/11045)
- [Adaptive walking control for quadruped robot by using oscillation patterns](https://www.nature.com/articles/s42256-022-00576-3)
- [AMP in the wild: Learning robust, agile, natural legged locomotion skills](https://arxiv.org/abs/2304.10888)
- [ARMP: Autoregressive Motion Planning for Quadruped Locomotion and Navigation in Complex Indoor Environments](https://arxiv.org/abs/2303.15900)
- [ArtPlanner: Robust Legged Robot Navigation in the Field](https://arxiv.org/abs/2303.01420)
- [ASC: Adaptive Skill Coordination for Robotic Mobile Manipulation](https://arxiv.org/abs/2304.00410)
- [Autonomous Stair Ascending and Descending by Quadruped Wheelchairs](https://ieeexplore.ieee.org/abstract/document/10202377)
- [Barkour: Benchmarking Animal-level Agility with Quadruped Robots](https://arxiv.org/abs/2305.14654)
- [Barry: A High-Payload and Agile Quadruped Robot](https://ieeexplore.ieee.org/document/10246325)
- [Combining model-predictive control and predictive reinforcement learning for stable quadrupedal robot locomotion](https://arxiv.org/abs/2307.07752)
- [Curiosity-Driven Learning of Joint Locomotion and Manipulation Tasks](https://openreview.net/forum?id=QG_ERxtDAP-&referrer=%5Bthe%20profile%20of%20Marco%20Hutter%5D(%2Fprofile%3Fid%3D~Marco_Hutter1))
- [DeepTransition: Viability Leads to the Emergence of Gait Transitions in Learning Anticipatory Quadrupedal Locomotion Skills](https://arxiv.org/abs/2306.07419)
- [DOC: Differentiable Optimal Control for Retargeting Motions onto Legged Robots](https://la.disneyresearch.com/wp-content/uploads/DOC_paper.pdf)
- [Dojo: A Differentiable Physics Engine for Robotics](https://arxiv.org/abs/2203.00806)
- [DreamWaQ: Learning Robust Quadrupedal Locomotion With Implicit Terrain Imagination via Deep Reinforcement Learning](https://arxiv.org/abs/2301.10602)
- [DribbleBot: Dynamic Legged Manipulation in the Wild](https://gmargo11.github.io/dribblebot/rsc/dribblebot_paper.pdf)
- [Drilling Task with a Quadruped Robot for Silage Face Measurements](https://www.researchgate.net/publication/370765569_Drilling_Task_with_a_Quadruped_Robot_for_Silage_Face_Measurements)
- [Event Camera-based Visual Odometry for Dynamic Motion Tracking of a Legged Robot Using Adaptive Time Surface](https://arxiv.org/abs/2305.08962)
- [Event-based Agile Object Catching with a Quadrupedal Robot](https://arxiv.org/abs/2303.17479)
- [Extreme Parkour with Legged Robots](https://arxiv.org/abs/2309.14341)
- [Fast Traversability Estimation for Wild Visual Navigation](https://arxiv.org/abs/2305.08510)
- [From Data-Fitting to Discovery: Interpreting the Neural Dynamics of Motor Control through Reinforcement Learning](https://arxiv.org/abs/2305.11107)
- [Geometric Mechanics of Contact-Switching Systems](https://arxiv.org/abs/2306.10276)
- [Guardians as You Fall: Active Mode Transition for Safe Falling](https://arxiv.org/abs/2310.04828)
- [Hierarchical Experience-informed Navigation for Multi-modal Quadrupedal Rebar Grid Traversal](https://arxiv.org/abs/2311.08354)
- [Identifying important sensory feedback for learning locomotion skills](https://www.nature.com/articles/s42256-023-00701-w)
- [Intelligent Control of Multilegged Robot Smooth Motion: A Review](https://ieeexplore.ieee.org/document/10216974)
- [iPlanner: Imperative Path Planning](https://arxiv.org/abs/2302.11434)
- [Language to Rewards for Robotic Skill Synthesis](https://arxiv.org/abs/2306.08647)
- [Layered Control for Cooperative Locomotion of Two Quadrupedal Robots: Centralized and Distributed Approaches](https://ieeexplore.ieee.org/document/10281391)
- [Learning a Single Policy for Diverse Behaviors on a Quadrupedal Robot using Scalable Motion Imitation](https://arxiv.org/abs/2303.15331)
- [Learning and Adapting Agile Locomotion Skills by Transferring Experience](https://arxiv.org/abs/2304.09834)
- [Learning Arm-Assisted Fall Damage Reduction and Recovery for Legged Mobile Manipulators](https://www.research-collection.ethz.ch/handle/20.500.11850/595246)
- [Learning Complex Motor Skills for Legged Robot Fall Recovery](https://ieeexplore.ieee.org/document/10138662/)
- [Learning Impulse-Reduced Gait for Quadruped Robot using CMA-ES](https://ieeexplore.ieee.org/abstract/document/10202519)
- [Learning quadrupedal locomotion on deformable terrain](https://www.science.org/doi/full/10.1126/scirobotics.ade2256)
- [Learning to Exploit Elastic Actuators for Quadruped Locomotion](https://arxiv.org/abs/2209.07171)
- [Learning to Walk by Steering: Perceptive Quadrupedal Locomotion in Dynamic Environments](https://arxiv.org/abs/2209.09233)
- [Legs as Manipulator: Pushing Quadrupedal Agility Beyond Locomotion](https://arxiv.org/abs/2303.11330)
- [LSC: Language-guided Skill Coordination](https://languageguidedskillcoordination.github.io/)
- [LSTP: Long Short-Term Motion Planning for Legged and Legged-Wheeled Systems](https://www.research-collection.ethz.ch/handle/20.500.11850/625515)
- [Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104)
- [Max: A Wheeled-Legged Quadruped Robot for Multimodal Agile Locomotion](https://ieeexplore.ieee.org/document/10375960)
- [Multi-Contact Whole Body Force Control for Position-Controlled Robots](https://arxiv.org/abs/2312.16465)
- [Not Only Rewards But Also Constraints: Applications on Legged Robot Locomotion](https://arxiv.org/abs/2308.12517)
- [OPT-Mimic: Imitation of Optimized Trajectories for Dynamic Quadruped Behaviors](https://arxiv.org/abs/2210.01247)
- [ORBIT: A Unified Simulation Framework for Interactive Robot Learning Environments](https://ieeexplore.ieee.org/abstract/document/10107764)
- [Orthrus: A Dual-arm Quadrupedal Robot for Mobile Manipulation and Entertainment Applications](https://ieeexplore.ieee.org/document/10309339)
- [PyPose: A Library for Robot Learning with Physics-based Optimization](https://arxiv.org/abs/2209.15428)
- [Real-Time Collision-Free Motion Planning and Control for Mobile Manipulation with Quadrupeds](https://ieeexplore.ieee.org/abstract/document/10354901)
- [Reinforcement Learning for Legged Robots: Motion Imitation from Model-Based Optimal Control](https://arxiv.org/abs/2305.10989)
- [Reinforcement Learning from Multiple Sensors via Joint Representations](https://arxiv.org/abs/2302.05342)
- [Resilient Legged Local Navigation: Learning to Traverse with Compromised Perception End-to-End](https://arxiv.org/abs/2310.03581)
- [Responsive CPG-Based Locomotion Control for Quadruped Robots](https://link.springer.com/chapter/10.1007/978-981-99-8073-4_22)
- [RL + Model-based Control: Using On-demand Optimal Control to Learn Versatile Legged Locomotion](https://arxiv.org/abs/2305.17842)
- [RoboHive: A Unified Framework for Robot Learning](https://arxiv.org/abs/2310.06828)
- [Robot Parkour Learning](https://openreview.net/forum?id=uo937r5eTE)
- [Robust Quadrupedal Locomotion via Risk-Averse Policy Learning](https://arxiv.org/abs/2308.09405)
- [Robust Recovery Motion Control for Quadrupedal Robots via Learned Terrain Imagination](https://arxiv.org/abs/2306.12712)
- [Roll-Drop: accounting for observation noise with a single parameter](https://arxiv.org/abs/2304.13150)
- [SafeSteps: Learning Safer Footstep Planning Policies for Legged Robots via Model-Based Priors](https://arxiv.org/abs/2307.12664.pdf)
- [SayTap: Language to Quadrupedal Locomotion](https://arxiv.org/abs/2306.07580)
- [Scientific Exploration of Challenging Planetary Analog Environments with a Team of Legged Robots](https://arxiv.org/abs/2307.10079)
- [Skill Graph for Real-world Quadrupedal Robot Reinforcement Learning](https://openreview.net/forum?id=vdm4WnG5u-M)
- [Solving Challenging Control Problems via Learning-based Motion Planning and Imitation](https://ieeexplore.ieee.org/abstract/document/10202250)
- [Taking the First Step Toward Autonomous Quadruped Robots: The Quadruped Robot Challenge at ICRA 2023 in London [Competitions]](https://doi.org/10.1109/MRA.2023.3293296)
- [Towards Legged Locomotion on Steep Planetary Terrain](https://www.research-collection.ethz.ch/handle/20.500.11850/625001)
- [Tuning Legged Locomotion Controllers via Safe Bayesian Optimization](https://arxiv.org/abs/2306.07092)
- [Versatile Multi-Contact Planning and Control for Legged Loco-Manipulation](https://www.science.org/doi/10.1126/scirobotics.adg5014)
"""

# 2. Ask the user for the title of the picture
# picture_title = input("Please provide the title for the picture (without the .png extension): ")
picture_title = "2023"

# 3. Extract the words from the titles (excluding the links)
titles = re.findall(r"\[(.*?)\]\(.*?\)", papers_input)

keywords = []
for title in titles:
    for word in title.split():
        cleaned_word = re.sub(r'[^a-zA-Z]', '', word).lower()  # Removing non-alphabetic characters and converting to lowercase
        if cleaned_word not in stopwords:
            keywords.append(cleaned_word)

# Counting keyword frequencies
keyword_freq = Counter(keywords)

# 4. Create the word cloud with landscape ratio and save it
wordcloud = WordCloud(width=2000,
                      height=500,
                      colormap="Blues",
                      background_color="rgba(255, 255, 255, 0)",
                      mode="RGBA").generate_from_frequencies(keyword_freq)
plt.figure(figsize=(20,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()

# Save the image in the same location as the code
file_name = f"{picture_title}.png"
plt.savefig(file_name, bbox_inches="tight", pad_inches=0, transparent=True)
print(f"Word cloud saved as {file_name}")
