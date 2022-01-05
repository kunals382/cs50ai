import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    product = 1
    probability = 0

    for person in people:
        gene = gene_number(person, one_gene, two_genes)

        if people[person]['mother'] is None and people[person]['father'] is None:
            probability = PROBS['gene'][gene] #* PROBS['trait'][gene][person in have_trait] 

        else: # if data about parents is available

            mother = people[person]['mother']
            father = people[person]['father']
            parents = [mother, father]
            parent_probabilities = {}
            
            for parent in parents:
                parent_probabilities[parent] = 0

                parent_gene = gene_number(parent, one_gene, two_genes)
                
                if parent_gene == 1:                    # 50/50 chance
                    parent_prob = 0.5 

                elif parent_gene == 0:                  # if 0 genes there’s a 1% chance it mutates into being the target gene. 
                    parent_prob = 0 + PROBS['mutation']

                elif parent_gene == 2: 
                    parent_prob = 1 - PROBS['mutation'] # if 2 genes there’s a 1% chance it mutates into not being the target gene anymore.

                parent_probabilities[parent] = parent_prob # storing probability of parents giving gene for each parent
    
            if gene == 0: # if none of the parents gave genes
                probability = (1 - parent_probabilities[mother]) * (1 - parent_probabilities[father])
                
            elif gene == 1: # if one of the parents gave genes
                probability = (1 - parent_probabilities[mother]) * parent_probabilities[father] + parent_probabilities[mother] * (1 - parent_probabilities[father])

            elif gene == 2: # if both of the parents gave genes 
                probability = parent_probabilities[father] * parent_probabilities[mother]

        probability = probability * PROBS['trait'][gene][person in have_trait] 
        product = probability * product    # multiply by probability of having the trait
        
    return product


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        probabilities[person]['trait'][person in have_trait] += p
        probabilities[person]['gene'][gene_number(person, one_gene, two_genes)] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait_sum = sum(probabilities[person]['trait'].values())
        gene_sum = sum(probabilities[person]['gene'].values())

        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] /= gene_sum

        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] /= trait_sum


def gene_number(person, one_gene, two_genes):
    if person in one_gene:
        gene = 1
    elif person in two_genes:
        gene = 2
    else: 
        gene = 0

    return gene       


if __name__ == "__main__":
    main()
