from transformers import pipeline

qa_model = pipeline("question-answering")
question = "List benefits related to reduce interference?"
context = """Benefits and Features 
● Meets Stringent Automotive OEM Module Power
Consumption and Performance Specifications
• 3.5µA Quiescent Current in Skip Mode at VOUT =
3.3V
• Fixed 5.0V/3.3V or Adjustable 1V to 10V Output
• ±1.1% Output-Voltage Accuracy for 5V Fixed
Setting
● Enables Crank-Ready Designs
• Wide Input Supply Range from 3.5V to 42V
● EMI Reduction Features Reduce Interference with
Sensitive Radio Bands without Sacrificing Wide Input
Voltage Range
• 50ns (typ) Minimum On-Time Allows
• Skip-Free Operation for 3.3V Output from Car
Battery at 2.2MHz
• Spread-Spectrum Option
• Frequency-Synchronization Input
• Resistor-Programmable Frequency Between
220kHz and 2.2MHz
● Integration and Thermally Enhanced Packages Save
Board Space and Cost
• 2MHz Step-Down Controller
• Current-Mode Controller with Forced-Continuous
and Skip Modes
• 16-Pin Side-Wettable (SW) TQFN-EP Package
• 20A Reference Design Available
● Protection Features Improve System Reliability
• Supply Undervoltage Lockout
• Overtemperature and Short-Circuit Protection
• Output Overvoltage and Undervoltage Monitoring
• -40°C to +125°C Grade 1 Automotive Temperature
Range
• AEC-Q100 Qualified"""
print(qa_model(question=question, context=context))

   