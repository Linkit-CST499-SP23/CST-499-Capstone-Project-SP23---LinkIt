# CST-499-Capstone-Project-SP23---LinkIt
LinkIt is a tool that automates the most labor-intensive manual tasks associated with data integration by examining disparate data, rationalizing the schema, and finding natural linkages. LinkIt provides an extensible framework so that the range of data it understands can be expanded over time – perhaps even by non-programmers.

## Running
```sh
python -m LinkIt
```

## BACKGROUND
The increasing value of data, data analytics, and machine learning is undeniable. Data is like raw ore that
can be mined, refined, and used to fuel the economy. Mining and refining real ore is hard and
the same is true for data, albeit for different reasons. In the case of data, the greatest value is
derived when multiple data sets are used together to create new insights. For example, imagine
a customer calls a support line at a company. The moment the support person answers the
phone, they ought to know whether there have been previous support calls, what products the
customer has purchased, how they rated the products, the sentiment of any reviews they have
written, and whether they have been offered any promotions. Armed with this information, the
support person has the greatest chance of providing a speedy and successful outcome.

That may not sound too difficult, but unfortunately, that data will be housed in at least 4 systems (sales,
support, product, marketing)1. Those systems almost certainly have incompatible data
organization, even if they were developed by the same organization! A company could just
mandate that all the different systems converge on a single data model, but repeated failures
show that such projects take years, cost millions, and are likely to start rotting almost as soon as
the project is complete.

Now consider that the company may also want to mine and integrate data from external sources. What
has the customer said about the product/company on Twitter? What’s the weather like in the
customer’s region (might affect some products or the ability to correct problems)? What do we
know about other people like that customer – how did we resolve their issues? Even more now
than before, we are guaranteed we will be working with lots of different schemas.
Integrating data is hard which is why there is a multi-billion dollar industry trying to address it.
