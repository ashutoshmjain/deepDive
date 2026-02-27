# Intrinsic and Google: The Roadmap for Physical AI

![Intrinsic Google Cover Image](./img/intrinsicGoogle.png)

The announcement of Intrinsic’s formal integration into Google marks a pivotal transition in the trajectory of industrial automation. This move signals the maturation of robotics from a specialized hardware discipline into a software-defined, AI-centric domain. This shift, described as the pursuit of "Physical AI," represents an effort to bridge the gap between the digital intelligence of large-scale neural networks and the complex, noisy reality of physical manipulation.

For decades, the industrial robotics sector has been characterized by high barriers to entry, proprietary programming environments, and a lack of interoperability. Intrinsic was founded to dismantle these barriers by creating a universal platform that simplifies robotic programming while enhancing the cognitive capabilities of the machines themselves. By joining forces with Google, Intrinsic gains access to unparalleled computational resources, foundational AI research, and a global infrastructure that positions it to redefine the global manufacturing and logistics landscape.

## **The Conceptual Framework of Physical AI**

To understand what Intrinsic does, one must first define the concept of Physical AI as it is applied in this context. Physical AI refers to the synthesis of advanced machine learning—including computer vision, reinforcement learning, and motion planning—with the mechanical execution of tasks in unstructured or semi-structured environments.

Historically, industrial robots have operated on a "blind and rigid" paradigm. They are programmed to move to precise coordinates ![][image1] with high repeatability, but they possess no inherent understanding of the objects they manipulate or the environment in which they operate. If a component is displaced by a few millimeters, the entire process fails.

Intrinsic’s platform introduces a layer of perception and adaptability that allows robots to "see," "feel," and "reason" about their tasks. This is achieved through a multi-modal software stack that processes sensor data in real-time to adjust robotic trajectories. The integration with Google accelerates this by bringing "Vision-Language-Action" (VLA) models into the industrial workspace.

These models, trained on vast datasets of both digital text and physical demonstrations, allow robots to understand high-level semantic instructions—such as "pick up the fragile object and place it gently"—and translate them into the precise motor commands required for execution.

### **Table 1: Transitioning from Traditional Automation to Physical AI**

| Feature | Traditional Industrial Automation | Intrinsic’s Physical AI Paradigm |
| :--- | :--- | :--- |
| Programming Method | Scripted, vendor-specific code (RAPID, KRL) | AI-driven, high-level intent and flow-based |
| Environmental Sensitivity | Requires highly structured, static cells | Adapts to dynamic, unstructured environments |
| Sensor Integration | Limited; often requires custom integration | Native multi-modal sensor fusion (vision, force, tactile) |
| Scalability | Low; code is hardware-dependent | High; code is hardware-agnostic and transferable |
| Learning Capability | None; requires manual re-programming | Continuous improvement via Sim2Real and fleet learning |
| Economic Barrier | High CAPEX and high integration costs | Reduced TCO through simplified development |

## **The Core Functional Capabilities of the Intrinsic Platform**

At its essence, Intrinsic provides a developer platform and an operating environment designed to make industrial robots as easy to program as a modern web application. This involves several distinct but interconnected technological pillars that work in concert to enable Physical AI.

### **Automated Motion Planning and Kinematics**

The most fundamental challenge in robotics is the mathematical translation of a desired end-effector position into the specific angles of each joint, known as inverse kinematics. For a standard six-axis industrial robot, the relationship between the joint angles ![][image2] and the Cartesian position ![][image3] is defined by the non-linear forward kinematics function ![][image4]. Solving the inverse, ![][image5], is computationally intensive and often has multiple solutions or singularities.

Intrinsic’s software automates these calculations, providing real-time collision avoidance and path optimization. Instead of a programmer manually defining every waypoint, they define the goal and the constraints (e.g., "move to this bin without hitting the safety railing"). The Intrinsic engine calculates the optimal trajectory in milliseconds, accounting for the robot's physical limits and the presence of obstacles detected by cameras.

### **Perception and Sensor Fusion**

For a robot to be "intelligent," it must have a high-fidelity representation of its surroundings. Intrinsic utilizes advanced computer vision algorithms to perform object detection, pose estimation, and semantic segmentation. This allows the system to identify not just where an object is, but what it is and how it should be handled.

Furthermore, Intrinsic places a heavy emphasis on force and torque sensing. By integrating feedback from sensors at the robot's wrist, the software can enable "active compliant" behaviors. This is critical for tasks like assembly, where a part must be "felt" into place, or polishing, where a constant force must be maintained across a curved surface. This combination of "seeing" and "feeling" mimics human dexterity.

### **Simulation-to-Reality (Sim2Real) Pipelines**

One of the greatest bottlenecks in AI for robotics is the data requirement. Training a reinforcement learning model on a physical robot is slow, expensive, and risks damaging the hardware. Intrinsic solves this through high-fidelity simulation. By creating a "digital twin" of the robot and its environment, millions of trials can be run in parallel in the cloud.

The challenge of Sim2Real is the "reality gap"—the small differences in physics, lighting, and sensor noise between the simulation and the real world. Intrinsic uses domain randomization and system identification techniques to ensure that models trained in the virtual world are robust enough to work on the factory floor. This allows for "zero-shot" deployment, where a robot can perform a new task correctly the first time it tries it.

## **Strategic Implications of the Merger with Google**

The decision for Intrinsic to join Google is a strategic realignment that recognizes the necessity of deep vertical integration between AI research and physical execution. While Intrinsic operated effectively as an independent Alphabet company, the move into Google provides three critical advantages.

### **Integration with Google Research and DeepMind**

Google is home to some of the world's most advanced AI research, particularly in the realm of foundation models. By integrating with Google Research, Intrinsic can directly leverage breakthroughs in Large Language Models (LLMs) and Vision-Language-Action (VLA) models like RT-2 and Gemini. These models enable a new level of "semantic intelligence" in robotics.

Imagine a warehouse where an operator can say, "Tidy up the workspace and organize the electronics by type." A traditional robot would have no way to process this. However, a VLA-powered Intrinsic system can use the LLM to decompose the high-level command into sub-tasks. This synergy transforms the robot from a scripted tool into an autonomous agent.

### **Computational Power and TPU Acceleration**

The training of physical AI models requires specialized hardware. Google’s Tensor Processing Units (TPUs) are designed specifically for the high-throughput matrix multiplications required by neural networks. By joining Google, Intrinsic can leverage this infrastructure to train larger, more capable models faster than any competitor.

### **Google Cloud and Enterprise Distribution**

Google Cloud provides the necessary backbone for managing large-scale robotic fleets across multiple geographic locations. For enterprise customers, the integration of Intrinsic into the Google Cloud ecosystem offers a familiar interface for monitoring performance and ensuring security. This moves robotics out of the "silo" of the factory floor and into the broader IT infrastructure.

### **Table 2: Synergies Generated by Intrinsic’s Integration into Google**

| Resource Area | Google’s Contribution | Impact on Intrinsic’s Roadmap |
| :--- | :--- | :--- |
| **AI Foundations** | Gemini, RT-2, and VLA model research | Higher semantic understanding and reasoning |
| **Compute** | Global TPU pods and specialized AI accelerators | Exponentially faster Sim2Real training cycles |
| **Data Ecosystem** | Google’s massive visual and linguistic datasets | Improved generalization for unstructured tasks |
| **Cloud Services** | Google Cloud Platform (GCP) infrastructure | Scalable fleet management and security |
| **Talent Pool** | World-class researchers in ML and robotics | Acceleration of core algorithm development |

## **The Acquisition Strategy: Vicarious and Open Robotics**

The roadmap of Intrinsic is also heavily influenced by its recent acquisitions, which have brought critical intellectual property into the fold. The integration of Vicarious and Open Robotics has effectively positioned Intrinsic at the center of the robotics ecosystem.

### **Vicarious: Generalizing Manipulation**

Vicarious was a pioneer in using brain-inspired AI to solve complex manipulation problems. Their focus was on architectures that allowed robots to generalize from a few examples rather than requiring millions of data points. This acquisition provides Intrinsic with advanced reasoning capabilities for tasks such as handling deformable objects like fabrics and plastics.

### **Open Robotics and the ROS Ecosystem**

The acquisition of Open Robotics (OSRC), the team behind the Robot Operating System (ROS) and the Gazebo simulator, was a seismic event. ROS is the de facto standard for robotics research and is increasingly being adopted for industrial applications.

By bringing the stewards of ROS into Intrinsic, Alphabet has ensured that its platform will be the most "ROS-friendly" environment in the world. This gives Intrinsic immediate credibility with the global developer community and allows it to lead the "industrialization" of ROS 2.

## **The Future Roadmap: Phases of Development**

The strategic roadmap for Intrinsic within Google can be viewed through three distinct phases: the Tooling Phase, the Cognitive Phase, and the Autonomous Ecosystem Phase.

### **Phase 1: Tooling and Standardization (Current-2 Years)**

The immediate priority is the stabilization and broad release of the "Intrinsic Flow" developer environment. This involves hardware abstraction for the "Big Four" manufacturers (Fanuc, Yaskawa, ABB, KUKA) and moving toward skill-based programming.

### **Phase 2: Cognitive Augmentation (2-5 Years)**

In this phase, the integration with Google’s VLA models becomes the primary differentiator. This includes natural language interfaces, visual reasoning for quality inspection, and cross-robot learning where skills are instantly adapted across different hardware forms.

### **Phase 3: The Autonomous Ecosystem (5-10 Years)**

The long-term vision is the creation of "self-optimizing" physical environments. This involves orchestrating entire facilities, autonomous process design from CAD drawings, and resilient manufacturing systems that can autonomously "work around" equipment failures.

### **Table 3: Roadmap Milestones and Expected Industrial Outcomes**

| Phase | Core Objective | Key Deliverables | Expected Industrial Impact |
| :--- | :--- | :--- | :--- |
| **Standardization** | Reduce integration friction | Universal Intrinsic API, ROS 2 Industrial | 50% reduction in deployment time |
| **Cognition** | Enhance task adaptability | VLA Model integration, Natural Language Control | Robots handle "high-mix" production |
| **Autonomy** | Full system orchestration | Self-synthesizing workflows, Fleet-wide optimization | Scalable "Lights-out" factories |

## **Technical Depth: The Mathematics of Adaptation**

To understand the "how" of Intrinsic’s roadmap, we must look at the mathematical frameworks they are employing. A key component is the use of Bayesian optimization and reinforcement learning (RL) in the Sim2Real pipeline.

In the RL framework, an agent (the robot) learns to maximize a reward function ![][image6]. The state of the system is ![][image7], and the agent takes an action ![][image8] according to a policy ![][image9]. The goal is to find the optimal policy ![][image10] that maximizes the expected return:

![][image11]

where ![][image12] is the discount factor and ![][image13] is a trajectory.

Intrinsic’s innovation lies in "Domain Randomization." During simulation, they vary the physical parameters ![][image14] (friction, mass, sensor noise) across a wide distribution ![][image15]. The agent is trained to maximize performance across this entire distribution, making it robust to real-world variations.

## **Strategic Positioning: The Alphabet-Tesla Rivalry in Physical AI**

The timing of Intrinsic’s reintegration into Google is widely viewed as a strategic consolidation intended to launch a coordinated offensive against Tesla’s Optimus humanoid platform and Amazon’s warehouse robotics. This positioning mirrors the rivalry between Waymo and Tesla’s Full Self-Driving (FSD) program.

*   **Platform Agnosticism vs. Vertical Integration:** Intrinsic aims to be the "Android of Robotics," providing a hardware-agnostic platform. In contrast, Tesla’s Optimus project is vertically integrated, aiming for unit costs as low as 30,000 dollars.
*   **Precision vs. Generalized Intelligence:** While Intrinsic emphasizes sub-millimeter precision and deterministic safety for complex manufacturing, Tesla focuses on "General-Purpose Autonomous Agents" derived from FSD neural networks.
*   **Operational Scale:** Intrinsic is focusing on the software layer to enable thousands of manufacturers, whereas Tesla aims to deploy a billion humanoid units by 2050.

## **Geopolitical and Economic Context: Reshoring and SMEs**

The "Physical AI" paradigm is a key enabler of "reshoring"—moving manufacturing back to high-wage countries. Traditionally, automation was only viable for high-volume products. By lowering the cost of programming and increasing flexibility, Intrinsic makes it economically feasible to automate "low-volume, high-mix" production.

### **Small and Medium Enterprises (SMEs)**

SMEs represent the "untapped frontier" of robotics. The average small machine shop often lacks robots because they cannot afford a full-time robotics engineer. Intrinsic’s low-code/no-code interface and pre-trained "skills" are designed specifically to empower these smaller players.

## **Challenges and Constraints in the Physical AI Roadmap**

Despite the resources of Alphabet, several challenges could impede execution.

### **The Safety-Performance Trade-off**

In the physical world, an AI error can result in catastrophic damage or injury. Bridging the gap between the probabilistic nature of deep learning and the deterministic requirements of industrial safety is a massive hurdle. Intrinsic is addressing this through "safety shields"—deterministic software layers that can override AI commands.

### **Data Privacy and Sovereignty**

As robots become cloud-connected, concerns about data privacy on the factory floor will intensify. Manufacturing processes are often guarded trade secrets. Intrinsic will need to provide robust guarantees that proprietary data is protected.

### **Hardware Limitations**

Software can only do so much if the underlying hardware is not up to the task. Traditional industrial robots were not designed for the high-speed, reactive control that Physical AI requires. The slow replacement cycle of industrial equipment means it will take years for the full potential of the software to be realized.

## **Conclusion: The New Era of Software-Defined Physical Systems**

The integration of Intrinsic into Google is a recognition that the future of robotics is a software problem. By combining the "brain" of Google’s AI research with the "nervous system" of Intrinsic’s robotic control platform, Alphabet is building the foundational infrastructure for the next industrial revolution.

Intrinsic’s success will be defined by its ability to create a "universal language" for the physical world, much as Android created a universal language for the mobile world. The transition to software-defined robotics is now a core strategic pillar of the digital-physical continuum.

#### **Works cited**

1. Intrinsic joins Google to accelerate the future of physical AI | Intrinsic, accessed February 27, 2026, [https://www.intrinsic.ai/blog/posts/intrinsic-joins-google-to-accelerate-physical-ai](https://www.intrinsic.ai/blog/posts/intrinsic-joins-google-to-accelerate-physical-ai)

2. Google DeepMind: Scaling Robotics with VLA Models, accessed February 27, 2026, [https://deepmind.google/discover/blog/scaling-robotics-with-vla-models/](https://deepmind.google/discover/blog/scaling-robotics-with-vla-models/)

3. The Android for Robotics: Intrinsic's Flowstate Platform, androidheadlines.com, accessed February 27, 2026, [https://www.androidheadlines.com/2026/02/google-intrinsic-robotics-physical-ai.html](https://www.androidheadlines.com/2026/02/google-intrinsic-robotics-physical-ai.html)

4. Google Astra and the Future of Embodied Reasoning, deepmind.google, accessed February 27, 2026, [https://deepmind.google/technologies/astra/](https://deepmind.google/technologies/astra/)

5. Open X-Embodiment: Robotic Learning at Scale, Google DeepMind, accessed February 27, 2026, [https://robotics-transformer-x.github.io/](https://robotics-transformer-x.github.io/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAADgklEQVR4Xu2YW6hNWxjHvxPKrVwjoROJhJDIPYUil5NrSjyQvCC5RhQPHsi9RCcSkgc8yUlS9oOc0zmlPLh0pA6JPKkTinL5//rm3GvMscdc1rZf7G3/6t/aa4w5xxzfN77xn2Nts1ZaCekstY8bmyHtpC5xYzVGSWetkTf9oBD8UWlh3JGin3RbGhZ3NGN6SH9I4+KOkF/Ms7Qnam8JzJJumm/nJMOlx9lnS4MtfFdaFnfkbJeuW8swuhT7pCtS27iDgAl8Z9wR0F+am30Ce2m21Kf+itrAhKZKY6Q2QTvbrlvUVgudpOlWmQfjY9pxkMz1mbmvFeBGOubFHeaT2iidlFZKD6UD0nlpm/REGlJ/dXUov4vSFvNxVgd906Q30oSg7VuMkJ5LX8zvZXFWSBvCizJI9gtpbKrjtTQ57hAzpV3mSYBz5oMMNa+Wd+b318JaabnUV/rPiuZKWTJug5UpgZU9YR4wizfD3NR+N1/9mNIFZvJkMBUEWRyc/U2J3bLK3pkk/Wa1lSrX7zafBMbz3iqrnG+7pnjOROmY+RxT5MGT/ALVgg8ZKL0yN8fvhSRckv6yykEqH7ea51SDVWcrdog7AvLgN8UdtQY/X/pg6e1RK3nJU+Y5mNEn8yAaA1txsbTX0qUeUlr2ZP6l+SRCGHyVdMr8gHDcfOIEAL2kI1LH7Dt0zVQGCcYnwkmQCFaeeeTwPN4oudfE0L5E2mzFbbfGfCvGlMVoPaUH5oYU0lt6Kt03d/R7Up35xHj4VivuIa7BODGuAUF7yEjpf6sE/6v0rxX3O0HzTKqszP0XSR+lf8xXngpgcdhOLEoMLk8sGHUBAuHHDDeHUEq4+zXphrTe/GEY3lVpR3ZNDk7NpD9borwyuJ7X5iPpjPmpkldV6CMkl/M445DgmEHSBam7eTCMxRh8Nggug0Wqs5IjLg78t/lBI4SSIpP5qsTfU1B6DcorAzcmAWwNxllgRecPwQPWxY3mzw6fz3hUb9lbJzfZPVF7PZTaHfMfAU2BBx20dNmPNj+MnM6+swq8m6mslFNziEolpbFQKWwHPkvBzS9beiK1QvL2W9qoqIa30hzzZxw2r7bUwQZvIElNmQswDzyBRKbmVE9uYqjqhSWw6kut/B8hlPwh6U/zlcBDyoLDM1JJaSxTzD2qbE4F2D+cvcfHHc0QXsm8RmsKvJWfha9HcJEccmCoZAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAA7ElEQVR4XuXRoYpCQRTG8bOgsOKCwgZd2GQQBJvYtNpMBgVfYTf7HhZBFkxisQqCxSaIZR/AoEUMNjUY3P2fOzM69z6B4Ac/HM89d2Y8ijxUXpBHDcnIs1sS6OEH31jgM9RB4uhjYNevmKDjN2ma2KNov+sVhpaug7xjiRFitvaGuaXrIC1c7afLBzbi7ag76E475O59UsYZXVfIYI0Ltp4j/tB2jSWcxHtTzCljHFBwxbqYI/QoF72r1qpeTSpixqI7a3ToUzGDdxMIondciXlBf90XZkj5TS4N/Iq5l/4b2fDjcHSo6WjxufMPwr0nO/SEKf8AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAAyklEQVR4Xu3RsQtBURTH8SMpokRSVslgYDAbKMrfIKtZFgMjo1JmyYBRFrNdKYPJ5A+wKJOB73n3vZIno+n96jPczjm3+84T8fLv+FFEDWH4kEUVobc+iWKJDno4YowhplgjqI16wwAla0wkhQtWyOOKHSJajKMv9iQp4IYGAmgiZ9dc0aa7mPf/jD5phj1iHzUr+nETtJDAScyADmp0G1qzUscTI5TxQNeu6UVzZOyzpHHAAhu0cRazsi0qTqMT3URSzI/5dvbiygvC9RzA6VnpHQAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEkAAAAYCAYAAAC2odCOAAADYUlEQVR4Xu2YS8hMYRzGH6EIySUREknhQxISFoRYkLBQLkt89ZXbQrnUFMpGyZ1IFEpKFi5FTCxcU4oSWRCKslGUJJ5n/uedec97zpyZWeh8k/nV03Te25zzv73vOUCLFi2q053qGzZm0JXqR3UJO5qVXtQCagzSH0rGOUFNCzsi0ubrdyu12WtrWkZQ96l91Edqfrwb3agj1Iag3TGDekSto67ADONQ9J2jlnttTUkBZqS91B9qZazXjFZEeqopst5S06PredRramh5BNBGPaCGe21NhWrGE+oUNZCaBKsljp7UTarDa3PIaPeow6ik01RYNOrXoUi8CHNGUzKW+kptCTsiplBvYONCVlM/YOnmWAyLRv36rII5Q05JIK/oj1TUVNxkcRU3hbC8lBc9qCGwm/8NSzFd9/YHkfWwVOwTtCuKHkby03AbzHB+JAlF6LuU9tLkCzAv7aCeUwdguX8aVuR0s3kwkzpJPaV+Uuej6/AhzkYKUfRonp7FoQDQOorMMPLkABlpmd+oCXuo2dG1G6TcnAhbqIik53x2Ue8bkGpH/9LM+pEBqqWB7q2IuCEccrzS6gsq//8paktbz62lSCujm92JSqQo3L7Bwlvb4hpqXNSXF0ohpdJlWHENSX2wCBk3jJhZ1C/qoNfmyDJ4GRnnO6w+dRaGUR+o7WFHRDUjufYwYgqwFPQLucPN0S6ailLvDJKL1kILK03r1SDEt+9aOM+HO5GjlpFUf9zW7wr5JVimhKSupUmHYKdQnT9ewgzlFtXupr4sJlArGtAiNLZjaudSCVApSEMpqFQMve/a/YK+kPpMTfbafNx5LHbU0A2riO2n5sA85qwoA+oPRkfXeaHaIefJidXQmGtI7sIdqNSywbBdMuvVQ6mtk7lO5GVGUc9gIXmV2gQ7lGnrv07NrQzNBZ3ZbqN60XYsoV4gaUg5WsbTfBloLbJfYpXacoj/ulJC1vfrRHidJ65oK+WyGEm9gj1kiJ5DxkurQSEF2PEnyyGdAnlaEX2LWgozUltsRBLN2Y34+1mjDKDuoHJm7NQoivWGrgJ6lDqG+jyrqLtLjQ876kTveMdRX8TljiKhnXoM23nTPn1UQ59EtL03Mkdoc7oB+2b1X6DNZmPYmIFO9DphKxJbtPhH/AWG46XKCOsYPwAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFsAAAAYCAYAAACV+oFbAAADu0lEQVR4Xu2YXahMURTHl1BEIfJRSi6RSCSiKE8ikZCPiAfJC14QodyS8kYSkhIlQlGIIiaEUPIgHkgk8uBFKBTW766z792z754758ydmXPV/OvXzJy9z5x91l5f54g01FCNNFhZo/QKBxqqnsYqV5SrSkHpWzQaF3Mq2ZR+Ss/wYCl1U8Yoc5Q+wVieqsa6Fkg6Y09STooZLqumKWckxbm9laPKCWWT8lAZXjQjH2HoLcol5aKYl7LWrEpjbO73jjI+HMig1cox6cDDGTgutqN8J4SuKdv9STlppPJBzAHeKY8khedEVM7YbOpBpTk4nlU4Ag6xOBxwWq58ViYkv7kw4QB8z1OrlK/KZGWKMjA5jtH2iDlJjM1Kj2QuKmds7v1V8tlZrVAeSMQpWPxj5ay0LY4FFRJKLa5eOqS8UYaEAxlVzthEMdFcSWEM1aS8VmaGA+zCn+TTaZhYyObl2VwTJxil3BPLo6QT2rfu3rws6sjYLm3uDAc8sR7+g0LN+ijUFOzR/qREjN2S4P/wZDz6k9huOE1Vfoh5VR5isbvFNvun8lQsNeyQ7MWxv7JfrOB/V06LdRy+nHNhzJgWidmJlHZfOaKcUzYqb5XZrTPbdEoCZyU0CdFfynuPb8pfsT8vJXYUI/jnlWNly5npRY7GQB2toxriOtSsdmEv1pkclrbugnSDA8wQc0bstDAZ88W8gniR5G7G92C8nRbrizLOO56HqOi/JW6Eago74Ax8hlqmzPJ+0xo/UQaIpZS1Eo82jO3mtYiwCT3YtVp+wcxL5DzWUut+vyNj+8JwGJAWuVwtw9hFhR1jk5vJ0U4USo75uxkThYqCRb5LS6w4lZKLsIJkO68SpTV2lrTWLo0QnuQqdxHC4YbYk2Q5r6aIzVeWZiBLWhqkvBAL21qrSfmozAsHxDqO82LOskHM2L69Dog5Xah9Yh1J6+sFXJwih9EJC6rrTYk04zmIjaFucIO1ltvY8FquhcMhJ4q9MqBrwfBoiVjXFKYU91DYrpvjhOdiIUuvObR4ODfhZVT9WhdHhHHIw6FxON6s3FYuK7uU6wnUNObHXoyR23lQjHUpLXmFfrQrieKIt+F19RC1CgO1dg+J3AOWy73h75hoC1+KNRtdViPEnhjXiUUa/W0YorUSBuSBZW44kFGsd29CvdZekXizRytKcXkm9vKpniLsL0i8b04rHvbI8zhOlxb9NHXjrlgXUG/hidsSKvFKnjLJ/SVfrzZULAy2VZkeDqTQeul8Gmqoof9I/wAUfrcRFI0NGgAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAABCElEQVR4XmNgGAWOQPwciP8j4VdA/AuI/wLxSSAOBmJmmAZsYA4Q/wZiGyQxkIY0BoghZUDMiCQHB7xAfBiI7wKxOJqcJBA/xCEHBppA/BaI1wAxC5qcKRB/A+KrQCyCJgcGfgwQv6ajSwBBAwNErhhNHA4mMWD6lxWIkxkgLiqF8jEADxAfYICE7jEo+zoDxLbpQCwMU4gNYPMvKFQrGSCh7AoVwwpg/i1CEzcG4q8MkCjECbD5FwSiGSCGtqKJwwG++AUZCtJcjiYOBzpA/J4BM35B7FUMqJqrgdgFxLBlgKQa9PQM8j8MgNIzKMBAhsQC8Wwg5kSSJwhAXvFlgIQ4SRpHATUAAIy9PJOevTuUAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAYCAYAAAAoG9cuAAAAp0lEQVR4XmNgGAXkAEYgVgDiACC2A2JWFFmowFQgXg7EIUBcB8RrgZgTWZEHEB8DYkEgZmGAKL4KxCLIisqB+CcQpwGxMBDrQjEKcAXiv0D8H4p3A7EoigooUAHiMiC+wgBRWASTADkM5MBbQCwGFQO56zQQp8MUiQPxbSCez4DwiQEQX2CAmAwGoLApZIDonAXEC4H4JBDbwxQgAw4glgRiAXSJ4Q0AAgEYuzqMmgwAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAZCAYAAAAIcL+IAAAAx0lEQVR4Xu3RMQtBURjG8VeYKIsYZVHKdidllDJQrMpqsbDJB7iTxcw38AXEcEerMimbbEaTgf/r3HM7mSwmnvp1nee87j1ckX++kTjKaCD1thelhB189BHggrEzIwUcMUEs7Hp4oG2HEljgjKItxdzpKuYor3w8qB+0WIn5kkavug6QDjtpiTnLwBYkjxPmThcNNp2uhju6qGKkZUXMo+2vy2CLGzxMUdcN/TuG2GOJDTo4YI0Zkjpoo4fOiXk7Gt3MOusfzBNijSGBwLzOUwAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAYCAYAAAC1Ft6mAAADDElEQVR4Xu2XS6hOURTHlzwihLwSQpSEKI+R14BiJhTFmAED3CIGuoqZTFCSEhMSAxED0k3yyEQiRQbMTChFGXj8f98629nfvufce75zDKT7q3/fd/fe5+y11l5r7e+aDfD/M1gaJw1KJ/qB9aOzz6rU3asyQ6Xj0qZ0ogKjpGPZZ1VwpEval33/6/Dyk1bv5XUcAoJ4SdqcTjRlvvRMmpVOVKSuQ7BAeixNTyfqwomczlTndKCJQ0Oky1J3Ml6bqdIbaW060QFNHILt5hlCkyiE3JwsTSnR2Hxpy5F30rRoLIX3LZVWZd9T+nKIU58pbbTy5xdJ76Vl6QQslj5Iv/rQPWlktv6g1GPFxsBq6YV509htnu+fpQ3RmjKHMP6MeUptkY5I16UR8SLzIONQrw47x9y49eYFfkVaLq2Rzll+QvHGF6Vr5rmcwrMfpa3RGK39q7QkGitzCDsemadSqJVX0oR4kflzPebBbWObNDv7Pk+6IA03j+ahsCgBh1BK2OSJNCYaP2+9jSpzCAO/Szul8dLCTClhL4JVyh7LFxy2Au8zyhyitn5a+yZEmuIlUHFHLHNonfTD8lS/K01sW+EEhwhWIUT0geWdC4M7dYj1OBR3P4r3i7QrGoMyh4AyOCC9NHdqf/t0i9KUC5C7tGJaMmBwmfecQNwkArwc43EiQHv9Zt6NqKtww6cOUfQUPzZMysbC6abBgDBX5Gyrs1y19kLHodfmrTyFDdKaAILyyfLin2FuIN2IW/2UeZ1C6hD7vDVPzdDR6L7PzU8shSuDqyPOhj9QdBhCgwhQT3SrudFYAIPZPBgXIDAnpIdemAblpfiJcCbelvZbXUeoQ4/zoJOp0V55/an4FFLHCPKgho9rgZRwhP88DGBd3qhjG6WSkUxFcwnSoYDxdM/4bUocCrE0v8iK6zVt6yKjG7DCPenrhVaXMoSoQnPvSynSiCRhyy7zN1qGJQwTzrBX/JGoERX8j++yUug7RIO5YvT0rQWM4Kg1LJ/qBWqFb8lkV/mXnyujrR/EA/zS/AazViZ4eGqWzAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAZCAYAAADTyxWqAAABA0lEQVR4XmNgGAX0BJOB2BhdkFRQBcQJQFwDxPZAPD+IVZAVkAJYgTgSiB8C8VIgVkSVJg0EAPFuIJ4OxIuAeBYQi6KoYIDYKA7EkjiwAFSdGhDzMUDCzASINYCYGyoHBgZA/AiI/+PBexhQNfkwQCxBAaDAOwDEHgwQ/68AYjMgdmCAeAHmMh6IcvwgAoiVoWxNBkjscACxJxBXwhQRC6hqGDLIAeJWKBuUnsqR5EgC/EB8CIhdoPyFDBQYBoqAW0AsDeWDDJuDkCYegNLYKiBeA8QsUDGQYdcZIGmPJKALxO8YIJEBA6DwewnE6khiRAFGIBYEYmYkMZBrQeE4CkYkAADruScqukKKtwAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAARCAYAAABgtvATAAADa0lEQVR4Xu3b0a3TMBjFcQ/AAgzAOxJD8MQCTMAGDAAbMAEbMMI3AivADjxDj5qjnPtdp03aSgj0/0nRtZ3EsV2kHLllDAAAAAAAAAD3e3E6vka9TsfH0/Ep2q6p3nDFy95wA/Xxe5zH2tvSj0mbaN4Vdd37LupaE49T9+e5mezvzen4sJ66ie5XP49wtJ/ZeonXY7bOqcb5Gq09AAB4gB7YHICOBLYMTXvdE9o8NgWC/uweEraCg0LMr6j3wJZqPF2jmexPa/o5zt0S3h4R+kzj0bFX9YZFrs9sTa3G+rwj/44AAMCGDGwZSjJQqV3BKHeaVM8QkPc6vOj6PJJf5H6++tU1vtdBTHXfr2td1j0ObL5P1FbR5sCmNvXr6y7tsPUwqfu3wpz1/vwcj7fGOlbPRW25tj1UObB5Dh6DrvP619Ku+/U31y65L9+r52ZgrShvhbEMX3mNnq26xllLXcfPKAMAgDtkYOsvageEijaHpB7Y/MLeS33ryOdnnxkmMpDoGo/TY5HZHNRH7rDlLpivtwxss68QHf629P5E9zhEJc1FfW3N3VT3NdXaM7CJ6i5nMLUMfxmGZ5+xfB/P55t1ramf71Dmeaotxw4AAO50KbB5R6WiTeVrgW3PDpuuVf9bocUvf/Wl8w5URwKbx+S2LKuvWsqSga0Hp37tzOwahaQMbBqrg+eewCaav9czv3I9Gthcz8CWc67lrzhIz/gzzsDW1SCwAQDwMHqZvhrry7y/XL0LVmN9UavswJA7Lv3ePRwMZqGl7455LDrUpjB0KbC53+yjljafV90yvEhFXffnuZnen/g/DuirQZUdpDwuqaWsZ6jcg5J+C/dlrDt8+uu5HQls4j5qPA9TXqNe7vL3g+LPRN7HOc9Pz5iNBQAA7KQXbe58+YVuKusFXeP8EvZXeZK/W3KQOMrhQX3pxe4+FW5UdrhR2dd5t+ntUs97dY367Dt6bnO4E/cj3vnKI0NHjeuBNPvLNocxB02P16FKf9WuUNbDmmgtdM6/B3NIyzXx/HV47fpYROc0nm/jfL6Wds8/57tF/x5ej6fr6Wc7NLruc2oDAAAPVONpsHHbJdUb/hEKOrOQ1G3tWHV7+/ubFMr659vNwh4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwP/gDcYwcPlbBnYEAAAAASUVORK5CYII=>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAAuklEQVR4XmNgGAX0BhxA7ADErkDMiSoFlgNhMHAC4tdA/B+K9wAxP1SOFYgnArEKiKMNxPeBuBWI9YE4AogfAXE5VLElELcAMSOI0wfEwVAJGAAZsAGIhYG4C4h1YBKCQMwM40AByBSQ1SBbQIpZUKUxQSkQn2GAOIMgCALiEwwIj+IFvkCcgy6IC9QAsQ26IDYA8vQ2INZEl8AGjIF4NwNEE0EQDcST0AVxgUIg9kAXxAVAkQSOXvoAAAo9FUIxQs5QAAAAAElFTkSuQmCC>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAAdUlEQVR4XmNgGAX0BqxALA7EklgwD5I6Bksgfg3E/3HgrUDMAVKoAsQHgNiDAWJKABBPhrJhGKwQBCKAWBnGAYJWIE5H4uMExkB8CYhl0CWwgXIgPgzEvOgS6IATiHcA8UJ0CWxAjQESIkS5lxmIhaH0KCAIAANMEb6CCCdSAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAA0UlEQVR4XmNgGAXUBHxA7AnEslA+NxC7AbExEDPDFHEC8VQgrgLiZ0DcAcRrgDgaSs8CYlaQQhcgrgZiTSB+C8RzoJpBwBSI30PVMCQAsRkQ+wHxX5ggFNgA8W8gLoIJgNy0hwFiFQtUDESD+CBbQLaBgRIQPwficpgAECgC8RMgns6A0Ay29j8QN0D5jEDcDMRXgFgeKgYGrQwQR58A4tVAfJABYq0EsiIeID4AxFsZIL4VhophAGzuwwrSGCDuiwNiATQ5FAAKeRiOQJMbDAAAPY4is2frKHoAAAAASUVORK5CYII=>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAABCklEQVR4Xu3SP0uCURTH8SPpVoTgGCQOge0Z7s0N6WZjQkOvoMm1oaX3IAg2tickOAhtYUjQEjRFiwUJmt/DeU7Y7SF7hqb6wWfw3PvcP94j8rezhB1cYIT3gNZa2PQPPBvooY0D3OIZdVRxjDuxRSao2Gci6xjiKPqdRR9XWPFJJIOG2AIdLGvxBE2sRpMKeMQ50lHNs4YH+brwR7bwKnbUML7waTjgqYkdbS8cIIcYiF01Nmd4QnGulsIu7lGaq3+K3kPv00FObId9XKKLvE+Mi+6mu17jBWOxt90W2/3b6H2nYs2SKPos+jw3YkdOFH+GRlD/UbTD3lAOBxZFu0v/Te02bcP//EZmmrIzfnCeV6oAAAAASUVORK5CYII=>
