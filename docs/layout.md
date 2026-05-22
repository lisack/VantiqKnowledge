# Layout Management User's Guide


## Background

An important part of developing Clients is laying out and positioning the Widgets. This can be problematic in large or complicated Pages, especially if the Widget sizes might change at runtime. For example, Widgets might change size because of the different data values they contain, programmatic changes by the Client itself, localization of static text, etc.

For some Page layouts, simple fixed positions for the Widgets is sufficient, but in most cases there is the need for some sort of "layout management" at runtime, where the sizes and positions of Widgets can change automatically as the need arises.

This requirement is usually driven by two basic approaches to layout:


* The most common approach assumes space is essentially unlimited (which corresponds to the "Browser" or "Mobile" Page Layout Types). In this case, your Page is a large scrollable area and the problem is to keep widgets from overlapping -- as they grow or shrink their positions must move to keep out of each others way. 

* Sometimes you want to avoid scrollbars and force the layout to conform to a fixed screen size. In this case, you would force a single 'outermost' container to a certain size (such as the browser window or the screen of a mobile device) and let children adapt within that space. This style corresponds to the "Single" Page Layout Type property.

The process of creating a layout has two phases:

* Decide what you want the Page to look like, what Widgets it must contain, how their positions relate to each other, and how the Widgets should respond when one or more of them change size or position. Deciding these issues can be far more complicated and difficult than you suppose. It can be a good idea to sketch out your plan to help visualize what you are trying to do.

* Determine how to implement this layout strategy using the Widgets and behaviors that are available in your toolkit. Vantiq Clients use the common approach of "layout containers" where each container provides the layout rules for the Widgets it contains.

This guide describes the Vantiq container Widgets and how you can use them to create a pleasing, dynamic layout.

## Layout Concepts

In order to understand the operation of layout containers there are several basic ideas you should be familiar with.


### Widgets

In general, Widgets decide what size they will be, and the containers they live in (their "parent") determines the position they will have.

### Layout Containers
Containers divide the space they control into cells, which is simply a rectangular region within the container.

Some kinds of Layout containers allow cells to be empty, but a cell can never hold more than a single Widget. A cell can be larger than the Widget it holds; in that case there are properties ("gravity") that determine where the Widget is positioned within the cell. (A Widget is never larger than the cell it occupies.) Cells are usually surrounded by margins provided by the container (because you usually don't want Widgets in a layout to be touching each other.)

Since layout containers are themselves Widgets, that means you can nest them; this ability creates a lot of power and flexibility with a simple set of containers.

#### VerticalLayout

In a VerticalLayout container all the cells are arranged vertically with each containing a single child Widget. (The optional Client "Side Bar" is actually a VerticalLayout container.)

<p><img style="border:none;" alt="VerticalLayout" src="../assets/img/layout/vertlayout.png" title="VerticalLayout"></p>

#### HorizontalLayout

In a HorizontalLayout container all the cells are arranged horizontally with each containing a single child Widget. (The optional Client "Top Bar" and the Page "Footer" areas are actually HorizontalLayout containers.)

<p><img style="border:none;" alt="HorizontalLayout" src="../assets/img/layout/horzlayout.png" title="HorizontalLayout"></p>

#### GridLayout

In a GridLayout container all the cells are arranged in a grid with a fixed number of rows and columns. It is possible for cells to be unoccupied.

<p><img style="border:none;" alt="GridLayout" src="../assets/img/layout/gridlayout.png" title="GridLayout"></p>

#### FixedLayout

Unlike the other layouts the FixedLayout container does not position its children at all; they stay wherever you put them. This means they may be "clipped" by their parent if their position is outside the bounds of the FixedLayout. This layout also implements the basic features of the FloorplanViewer which means you can bind it to a Data Stream and automatically display markers based on the input data.

This container is intended for use as an advanced kind of FloorplanViewer; a common use case would be to give the FixedLayout a large image to serve as the background "floor plan" and then use a combination of "markers" (driven by a Data Stream) and programmatically created children (such as StaticIcons and Canvases) and then explicitly positioning them. Typically you would make a FixedLayout the top level widget for a "Single Layout" Page. If you then turn on the Single Layout's "zoom to fit" option then the contents of the FixedLayout (background, markers and children) will be scaled to fit the available space.



#### FlowLayout

In a FlowLayout container all the cells are arranged left-to-right and then top-to-bottom. Cells are never empty in a FlowLayout. This layout style is similar to the behavior of a standard "div" element in HTML where the width is fixed and then the widgets "flow" into the space, wrapping as needed and then stretching the height of the FlowLayout to fit the contents. (The FlowLayout has a width policy of "Explicit" by default.)

<p><img style="border:none;" alt="FlowLayout" src="../assets/img/layout/flowlayout.png" title="FlowLayout"></p>

### Natural Size
Each type of Widget computes for itself a "natural size". That means it chooses a height and width based on its current properties to give a pleasing effect without truncating any graphical features. (For example, a Button can be no smaller than the minimum space needed for its label, padding and other parts.) Some Widgets can be stretched to be larger than their natural size. (A Button can be wider than its default but not taller.)

### Size Policies
Widgets have one of 3 possible "size policies" for both width and height that determine different ways to select the actual final size for each:

#### Natural
Choose the minimum dimensions appropriate for this Widget type, taking the particular graphical features of the Widget into account.

#### Explicit
Allow the dimension to be explicitly set (in pixels) by the developer. (The explicit size can't be any smaller than the natural size for the widget, only larger.)

#### Size to Parent
When the Widget's parent is a Layout container, this policy causes the Widget to stretch to fill the cell it occupies. (When the Widget's parent is not a Layout container with cells, this policy is treated as "Natural Size".)

Not all Widgets allow you to set all possible size policies. For example, Buttons only support a "height policy" of "Natural Size" but their "width policy" can be any of the three.

### Gravity
When the cell a Widget occupies is larger than the Widget itself, there is a choice to be made about where the Widget will be positioned within it. In this situation, there is a property called Gravity that is used to make the decision.

* "Horizontal Gravity" can be Left, Right or Center
* "Vertical Gravity" can be Top, Bottom or Center

In the example below are 3 VerticalLayouts, each with some StaticText and a Button. The Button has a width policy of "Natural" so the cell it resides in is wider than the Button itself. They show the effect of changing the horizontal gravity of the Button.

<p><img style="border:none;" alt="Gravity" src="../assets/img/layout/gravity.png" title="Gravity"></p>

See the section below on [Cells](#cells) for more details.

### Weight
Normally a  container's cells will be just large enough to hold the Widgets inside. But if a container has a Size Policy other than "Natural" then it may be larger than necessary to hold all of its children; in that case, there will be some "excess space" that must be divided up between them. By default, all the extra space will be divided up equally between all the cells.

But sometimes that's not what you want. It may be appropriate for all of the "extra" space to go to a single cell and all the others to remain at their "natural" size. Or perhaps two cells should get half of the space and the rest none.

"Weight" is how you specify the behavior you want. This property is used to calculate what fraction of the space should go to each cell. We do this by "normalizing" the weights; the fraction of the extra space going to a cell is equals to its "weight" divided by the total of all the weights.

For example, if there are three cells with weights "0", "1" and "1" then the extra space will be allocated as "0%", "50%" and "50%". (Because the total weight is 0+1+1=2, making each fraction 0/2, 1/2 and 1/2.)

A set of examples is below. 

<p><img style="border:none;" alt="Weight" src="../assets/img/layout/weight.png" title="Weight"></p>

In Case 1 we have a HorizontalLayout which contains 3 Buttons, all of which have a width policy of "Size to Cell". Since the HorizontalLayout has a width policy of "Natural Size" all the Buttons are their minimum, natural size as well.  

In Case 2 we change the HorizontalLayout's width policy to "Explicit" so we can manually make it wider and see what happens to the Buttons inside. All 3 Buttons have their default weight of zero so they all share equally in the extra space.

In Case 3 the last button has been given a horizontal weight of 1, which means it now gets 100% of the extra space. (Leaving the other Buttons only the space required by their natural size.)

In Case 4 the second button has been given a weight of 1 as well, which causes Button 2 and Button 3 to now both get 50% of the extra space.

See the section below on [Cells](#cells) for more details.

### Margins

By default the layout containers insert extra margins between the cells so their children won't be touching.

* Inner Margin - The margin between cells
* Top-Bottom Margin - The margin at the top and bottom edge of the layout (above and below all the cells)
* Left-Right Margin - The margin at the left and right edge of the layout (to either side of all cells)



### Cells

The GridLayout, VerticalLayout and HorizontalLayouts use a concept called a "cell" - this is the area that gets set aside for each of the container's child widgets. Understanding this idea makes it easier to see how Gravity and Weight affect the layout.

For example, let's look at a VerticalLayout with 3 child widgets. By default the VerticalLayout has a HeightPolicy of "Natural" which means that it shrinks down to the minimum size needed to contain its children. When laying out the positions of its children the VerticalLayout starts by creating "cells" to hold each child:

<p><img style="border:none;" alt="Cells" src="../assets/img/layout/cell1.png" title="Default Cells"></p>

For the rest of the example images we will draw in the cell boundaries with a dotted line so you can see where the are.
Note that by default there are margins set around and between the cells; the cells themselves don't have margins:

<p><img style="border:none;" alt="Cells" src="../assets/img/layout/cell2.png" title="Default Cells"></p>

So far the cells exactly contain the child widgets because the VerticalLayout is no larger than needed to hold the children and the margins. But now let's give the VerticalLayout a HeightPolicy of "Explicit" and manually increase its size:

<p><img style="border:none;" alt="Cells" src="../assets/img/layout/cell3.png" title="Expanded VerticalLayout"></p>

In this case there is now "extra" vertical space; by default the VerticalLayout divides this extra space equally and adds it to the height of each child's cell. Since the cells are now larger than the child widgets they contain there is a question as to **where** within the cell each child should be positioned. This is where Gravity comes in; by default each child has a VerticalGravity of "Center" so they are vertically centered within their cell.

However if we change the VerticalGravity of the first child (the InputString) to "Top" it will look like this:

<p><img style="border:none;" alt="Cells" src="../assets/img/layout/cell4.png" title="Expanded VerticalLayout with Gravity"></p>

The key point is that "Gravity" indicates where a child should be positioned **within its cell**. 

As we noted above, by default this extra vertical space is allocated equally to each cell. But by using the VerticalWeight property we can change this. For example, if you select the 3rd child (the StaticText widget) and change its VerticalWeight to 1 (leaving the other 2 children set to the default of 0) then **all** the excess space will be assigned to the 3rd cell, giving this:

<p><img style="border:none;" alt="Cells" src="../assets/img/layout/cell5.png" title="Expanded VerticalLayout with Weight"></p>

Note that the VerticalGravity of "Top" we set on the InputString is now meaningless since the cell it lives in no longer affords it any extra vertical space.


### isVisible
There are times when you want to make a Widget temporarily disappear from the Page. Widgets have a Boolean property called "isVisible" which you set to "false" to hide them. When layout containers manage their space, they ignore such "invisible" children, pretending as if they aren't even there.

### Page Layout Type

Client Pages offer 3 different ways to approach widget layout:

* Browser - The page presents a large canvas on which to place your widgets. In this style your Widgets can be placed anywhere you want and the Browser "viewport" may need to be scrolled to see them all. This layout is best suited to large "dashboard" Pages. 
* Mobile - This style is intended for use with Clients which are targeted at mobile device users rather than a browser. The page presents a single Vertical Layout container where you place your widgets, and the width of the Vertical Layout will always be stretched to fit the width of your device. The widgets are arranged into a vertical scrollable list (which is a common pattern on mobile devices).
* Single - This style is most useful when constructing pages which you want to exhibit "Responsive Design". You are allowed to place a single widget on the Page; when you set its Size Policies to "Size to Parent" the widget will always be stretched to fit the viewport. See the [Reponsive Design](#responsive-design) section below for a more complete discussion.

## Responsive Design

A common requirement is to have your layout conform to the "viewport" presented by the browser or mobile device. The best way to accomplish this is set the Page to the "Single" Layout Type; this means the Page can only contain a single child (but the child could be a container which contains more widgets inside). This single "root" widget would commonly be given a Height and Width policy of "Size to Parent" so it would always conform to the viewport.

By using a Grid Layout as your root widget and adjusting various layout properties (such as "width policy", "height policy" and "weight") you can create many arrangements that will automatically adjust to the size of the viewport.

In the case of a browser that means that the Page can adapt to the Browser window as the user resizes it. On a mobile device it means the Page will conform to the specific height and width of a phone, and react when the user rotates the phone from "Portrait" to "Landscape".


## Example - Simple Form Layout

This example shows how you might construct a simple, standard "form layout". Here's the final result we are aiming for, followed by the steps it would take to build it from scratch.

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid7.png" title="Final Layout"></p>


### Step 1: Create a Grid Widget

Create a Grid Widget. By default it has 2 rows and 2 columns. The Grid is initially empty, but the empty cells are made large enough so you can easily drop in a new Widget.)

When in the Client Builder you will see dashed lines outlining each "cell" within the Grid; this makes it easier to visualize what we are doing while editing. When the Client is running these lines disappear. (You can turn them off in the Client Property sheet if you'd rather not see them.) There are gaps between the cells because by default the Grid sets aside some space for margins; you can adjust these in the Grid's property sheet.


<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid1.png" title="Grid Example Step 1"></p>

### Step 2: Change the Grid size

Select the Grid and change it to 4 rows and 2 columns.

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid2.png" title="Grid Example Step 2"></p>


### Step 3: Add widgets to the Grid


Populate the Grid with some StaticText and InputString Widgets (so it will look like a standard "input form").

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid3.png" title="Grid Example Step 3"></p>


### Step 4: Change the text widgets

Change the StaticText widgets so they are all different. This makes them all different widths, which means they no longer line up.

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid4.png" title="Grid Example Step 4"></p>



### Step 5: Change the text Gravity

Select each of StaticText widgets and change their "Horizontal Gravity" property to "Left", making them all align to the left side.


<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid5.png" title="Grid Example Step 5"></p>



### Step 6: Make the Grid resizable

Change the "Width Policy" of the Grid to "Explicit". Now you can grab the Grid's right edge and make it wider than the current minimum "natural" size. Note that all the extra horizontal space has been divided equally between the two columns. (The InputStrings have a default Width Policy of "Size to Cell" so they all all stretched to fill the second column.)

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid6.png" title="Grid Example Step 6"></p>


### Step 7: Adjust the Weights

Set the "Horizontal Weight" of the InputString Widgets to "1", which forces all the extra horizontal space to be allocated to the second column. (Note that you don't actually have to change the weights of **all** the Widgets; the Grid only pays attention to the **largest** Horizontal Weight in a column, so you only need to set one of them. For a row it only respects the largest **Vertical** Weight.) 

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid7.png" title="Grid Example Step 7"></p>

When the Client is running the "cell outlines" will disappear:

<p><img style="border:none;" alt="Grid Example" src="../assets/img/layout/grid8.png" title="Grid Example Step 8"></p>


## Example - Responsive Design Layout using a Grid Container

This example shows how you can use a Grid Container and a Page with the "Single" Layout to build a common "responsive design" layout that will adapt to changes in the viewport size.

It's always a good idea to plan roughly your layout in advance. Divide the space into "zones" which will contain all your widgets, and then know what you want to happen when the overall layout changes size. For our example we will assume our Page is divided into 5 zones like this:

<p><img style="border:none;" alt="Responsive Design Example Step XX" src="../assets/img/layout/small.png" title="Responsive Design Example Step 1"></p>

When the Page is stretched to fill the viewport we would like only the center area to grow and the four surrounding areas to stay mostly the same. Like this:

<p><img style="border:none;" alt="Responsive Design Example Step XX" src="../assets/img/layout/large.png" title="Responsive Design Example Step 1"></p>

For example, let's say we are building a Page whose final form should look like this, with a map in the center, a title at the top and controls around the outside. Something like this:


<p><img XXstyle="border:none;max-width:none;" alt="Responsive Design Example Step 1" src="../assets/img/layout/rd15.png" title="Responsive Design Example Step 1"></p>


Below we outline all the steps to create such a layout in the Client Builder.

### Step 1: Create a Page with the "Single" Layout Type

The editing area starts out empty:

<p><img style="border:none;" alt="Responsive Design Example Step 1" src="../assets/img/layout/rd01.png" title="Responsive Design Example Step 1"></p>


### Step 2: Add a Grid Container Widget

Because we set the Layout Type to "Single" we are only allowed to add a single widget to the page; in this case that means we should add a Grid Container Widget, which will have all the power we need to build the target layout. The Client Builder automatically sets the Grid's Height and Width Policy to "Size to Parent" so it will fill the entire Page. 

If the contents of the single widget force it to be larger than the browser viewport then scrollbars will be added automatically. As an alternative you can turn on the "Zoom To Fit (at runtime)" option in the Page's property sheet which will **scale** the widget and it's contents so it will always fit within the space provided.

When in the Client Builder you will see dashed lines outlining each "cell" within the Grid; this makes it easier to visualize what we are doing while editing. When the Client is running these lines disappear. (You can turn them off in the Client Property sheet if you'd rather not see them.) There are gaps between the cells because by default the Grid sets aside some space for margins; you can adjust these in the Grid's property sheet.

By default the Grid has 2 rows and 2 columns and so looks like this:

<p><img style="border:none;" alt="Responsive Design Example Step 2" src="../assets/img/layout/rd02.png" title="Responsive Design Example Step 2"></p>

### Step 3: Set the Grid's size

In order to build our target layout we must adjust the Grid to be 3x3 instead of 2x2. The layout will look better if we also set the Grid's border size to 0.

<p><img style="border:none;" alt="Responsive Design Example Step 3" src="../assets/img/layout/rd03.png" title="Responsive Design Example Step 3"></p>

### Step 4: Add some title text

Add a StaticText widget to the cell in the upper-left corner and set the text for the title.

<p><img style="border:none;" alt="Responsive Design Example Step 4" src="../assets/img/layout/rd04.png" title="Responsive Design Example Step 4"></p>

### Step 5: Set the Title's "column span"

We want the title to span the entire "top" zone of the layout, so select the text and use its property sheet to change its "column span" from 1 to 3. This means the StaticText will always occupy 3 cells horizontally. By default it will be centered within this space:

<p><img style="border:none;" alt="Responsive Design Example Step 5" src="../assets/img/layout/rd05.png" title="Responsive Design Example Step 5"></p>

### Step 6: Add a Button

Now add a Button to the cell in the lower-left corner. (Note that by default its "width policy" is "size to parent" so it fills the entire cell.)

<p><img style="border:none;" alt="Responsive Design Example Step 6" src="../assets/img/layout/rd06.png" title="Responsive Design Example Step 6"></p>

### Step 7: Set the Title's "column span"

Just like we did with the title text above change the Button's "column span" from 1 to 3. At the same time we can change the button label to "Done" and set the "width policy" to "Natural" so the Button will be no wider than it needs to be.

<p><img style="border:none;" alt="Responsive Design Example Step 7" src="../assets/img/layout/rd07.png" title="Responsive Design Example Step 7"></p>

### Step 8: Add 2 sets of controls

We wanted a set of buttons in each of the "left" and "right" zones. One way to do that is to add a Vertical Layout into each of the two zones. Add two Menu Buttons into each and give them their own titles:

<p><img style="border:none;" alt="Responsive Design Example Step 8" src="../assets/img/layout/rd08.png" title="Responsive Design Example Step 8"></p>

### Step 9: Add Map to the center cell

Add a Map widget to the center cell:

<p><img style="border:none;" alt="Responsive Design Example Step 9" src="../assets/img/layout/rd09.png" title="Responsive Design Example Step 9"></p>

### Step 10: Adjust the left and right "control" containers

Since we probably don't want the two Vertical Layouts in the "left" and "right" zones to float in the middle of their cells we can set their "vertical gravity" to "Top" and then set their "width policy" to "size to parent":

<p><img style="border:none;" alt="Responsive Design Example Step 10" src="../assets/img/layout/rd10.png" title="Responsive Design Example Step 10"></p>

### Step 11: Remove borders

The borders don't add anything so we can remove them:

<p><img style="border:none;" alt="Responsive Design Example Step 11" src="../assets/img/layout/rd11.png" title="Responsive Design Example Step 11"></p>

### Step 12: Set Map Size Policies

We want the Map in the center to fill up the central cell, so change both its height and width policies to "size to parent":

<p><img style="border:none;" alt="Responsive Design Example Step 12" src="../assets/img/layout/rd12.png" title="Responsive Design Example Step 12"></p>

### Step 13: Adjust the Map's "weight"

When the Grid gets resized we would like all the "extra" space to be allocated to the Map in the central cell. We specify this behavior by setting the Map's horizontal and vertical weight to 1 and leaving all the other cell weights at 0. (There is an explanation of how "weights" work [here](#weight).)

With that last change we are done:

<p><img style="border:none;" alt="Responsive Design Example Step 13" src="../assets/img/layout/rd13.png" title="Responsive Design Example Step 13"></p>

### Step 14: Test the layout

In order to see if we got the effect we want you can just resize the Client Builder pane and see what happens to the layout. Try some different widths and heights to see if it reacts the way you expect:

<p><img style="border:none;max-width:none;" alt="Responsive Design Example Step 14" src="../assets/img/layout/rd14a.png" title="Responsive Design Example Step 14a"></p>


<p><img style="border:none;max-width:none;" alt="Responsive Design Example Step 14b" src="../assets/img/layout/rd14b.png" title="Responsive Design Example Step 14b"></p>


<p><img style="border:none;max-width:none;" alt="Responsive Design Example Step 14c" src="../assets/img/layout/rd14c.png" title="Responsive Design Example Step 14c"></p>

### Step 15: Run the Client

The final step is the run the Client; this will make the cell outlines disappear so you can see how the Client really looks to the user:

<p><img XXstyle="border:none;max-width:none;" alt="Responsive Design Example Step 15" src="../assets/img/layout/rd15.png" title="Responsive Design Example Step 15"></p>
