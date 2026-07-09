# Guide

## Products
Specify the name, then the set of properties. Property names must be unique. Also, specify the name of the unions.
```python
# primitive parts
rocker_arm_top = Product("rocker_arm_top", {("rocker_arm_top_length", 6), ("rocker_arm_top_height", 2), ("rocker_arm_top_rotation_speed", 2)})
spring = Product("spring", {("spring_length", 3), ("spring_radius", 1), ("spring_k", 5)})
valve = Product("valve", {("valve_base_radius", 1), ("valve_radius", 0.2), ("valve_length", 5), ("valve_translation_period", 2)})
tappet = Product("tappet", {("tappet_length", 5), ("tappet_radius", 0.2)})
roller = Product("roller", {("roller_radius", 0.5)})
socket = Product("socket", {("socket_length", 1)})
cam_body = Product("cam_body", {("cam_body_shape", "blablabla"), ("cam_body_material", "steel")})
cam_key = Product("cam_key", {("cam_key_radius", 0.5)})
cam_shaft = Product("cam_shaft", {("cam_shaft_radius", 0.5)})

# intermediate parts
cam = cam_body.get_union("cam", cam_key, cam_shaft)
follower = socket.get_union("follower", roller)

# full product
rocker_arm = rocker_arm_top.get_union("rocker_arm", spring, valve, tappet, follower, cam)

# get aggregated properties
print(rocker_arm.get_elements())
```

## Nature
Nature_Prime is the representation of nature inside human thought. It takes an arbitrary amount of products, and aggregates them. We've created an Object called "environment", using the Product subclass, because it's faster. Obviously, it's not actually going to be used as a product.
```python
nature_prime = Nature_Prime(rocker_arm, Product("environment", {("temperature", 21)}))

# Environment is defined by taking the complement of the product inside nature
environment = Environment(valve, nature_prime)
```

## Relations and performances
```python
# Create a relation
relation = Relation(rocker_arm_top, valve)

# Get structure
# Union of set with the Cartesian product on itself
struct = rocker_arm.structure()

# Get actions, responses, performances
# These are Cartesian products
actions = Actions(rocker_arm, environment)
responses = Responses(rocker_arm, environment)
performances = Performances(actions, responses)
```

## Requirements
To create a requirement, use one of the predefined templates for requirements. They're all inherited from a general requirement class. Currently, there are range requirements (for numbers falling within a range), and equality requirements (for properties that must equal to a value).
```python
spring_force_requirement = Num_Range_Specification("spring_k", 4, 5)
cam_body_shape_requirement = Equality_Specification("cam_body_shape", "egg")
cam_body_material_requirement = Equality_Specification("cam_body_material", "steel")

print("Spring force satisfied: " + str(spring_force_requirement.evaluate(rocker_arm)))
print("Cam body shape satisfied: " + str(cam_body_shape_requirement.evaluate(rocker_arm)))
print("Cam body material satisfied: " + str(cam_body_material_requirement.evaluate(rocker_arm)))
```

## Editing and viewing
```python
# Equality and inequality
print(rocker_arm.equals(cam_body))
print(rocker_arm.unequal(cam_body))

# Children
print("Children: ", end="")
for child in rocker_arm.get_children():
    print(child.name, end=", ")
print("")

# Get further complexity descendants
print("2nd-complexity children: ", end="")
for child in rocker_arm.get_level(2):
    print(child.name, end=", ")
print("")

# Verify primitivity
print(valve.is_primitive())
print(rocker_arm.is_primitive())

# Removing and inserting children
cam.remove_child(cam_body)
print(cam.get_elements())
cam.insert_child(cam_body)
print(cam.get_elements())

# Get product property (from aggregated)
print(rocker_arm.get_property("valve_base_radius"))

# Get own properties
print(valve.get_own_properties())

# Update property (from aggregated)
# Creates a new property if does not exist
rocker_arm.search_from_name("valve").update_property("valve_length", 10)
print(valve.get_own_properties())

# Delete property (from aggregated)
rocker_arm.search_from_name("valve").delete_property("valve_length", 10)
print(valve.get_own_properties())

# Get path to root
print(cam_key.path())
```
