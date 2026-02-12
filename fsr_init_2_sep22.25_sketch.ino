/* FSR testing sketch with averaging */

int fsrPin = A0;     // analog pin
const int numSamples = 50;   // number of samples to average
long totalReading = 0;
int fsrReading = 0;
long fsrVoltage = 0;
unsigned long fsrResistance;
unsigned long fsrConductance;
long fsrForce;

void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  totalReading = 0;

  // Take multiple samples and sum them
  for (int i = 0; i < numSamples; i++) {
    totalReading += analogRead(fsrPin);
    delay(5);  // small delay between readings (5 ms)
  }

  // Compute average
  fsrReading = totalReading / numSamples;

  Serial.print("Average analog reading = ");
  Serial.println(fsrReading);

  // Convert to voltage in mV
  fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
  Serial.print("Average voltage (mV) = ");
  Serial.println(fsrVoltage);

  if (fsrVoltage == 0) {
    Serial.println("No pressure");
  } else {
    fsrResistance = (5000 - fsrVoltage) * 10000L / fsrVoltage;
    Serial.print("FSR resistance (ohms) = ");
    Serial.println(fsrResistance);

    fsrConductance = 1000000L / fsrResistance;
    Serial.print("Conductance (microMhos): ");
    Serial.println(fsrConductance);
  }

  Serial.println("--------------------");
  delay(500);
}
